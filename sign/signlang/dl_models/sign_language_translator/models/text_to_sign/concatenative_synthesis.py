"""This module defines the ConcatenativeSynthesis class, which represents a rule based model for translating text to sign language."""

from __future__ import annotations

import random
from enum import Enum
from typing import List, Type, Union

from sign_language_translator.config.enums import (
    SignEmbeddingModels,
    SignFormats,
    normalize_short_code,
)
from sign_language_translator.languages import get_sign_language, get_text_language
from sign_language_translator.languages.sign import SignLanguage
from sign_language_translator.languages.text import TextLanguage
from sign_language_translator.models.text_to_sign.t2s_model import TextToSignModel
from sign_language_translator.vision._utils import get_sign_wrapper_class
from sign_language_translator.vision.sign.sign import Sign


class ConcatenativeSynthesis(TextToSignModel):
    def __init__(
        self,
        text_language: Union[str, TextLanguage, Enum],
        sign_language: Union[str, SignLanguage, Enum],
        sign_format: Union[str, Type[Sign]],
        sign_embedding_model: Union[str, Enum, None] = None,
    ) -> None:
        self._text_language = None
        self._sign_language = None
        self._sign_format = None
        self._sign_embedding_model = None

        self.text_language = text_language
        self.sign_language = sign_language
        self.sign_format = sign_format
        self.sign_embedding_model = sign_embedding_model
    @property
    def text_language(self) -> TextLanguage:
        if self._text_language is None:
            raise ValueError("Text language is not set.")
        return self._text_language
    @text_language.setter
    def text_language(self, text_language: Union[str, TextLanguage, Enum]):
        self._text_language = self.__get_text_language_object(text_language)
    @property
    def sign_language(self) -> SignLanguage:
        if self._sign_language is None:
            raise ValueError("Sign language is not set.")
        return self._sign_language

    @sign_language.setter
    def sign_language(self, sign_language: Union[str, SignLanguage, Enum]):
        self._sign_language = self.__get_sign_language_object(sign_language)
    @property
    def sign_format(self) -> Type[Sign]:
        
        if self._sign_format is None:
            raise ValueError("Sign format is not set.")
        return self._sign_format

    @sign_format.setter
    def sign_format(self, sign_format: Union[str, Type[Sign], Enum]) -> None:
        self._sign_format = self.__get_sign_format_class(sign_format)

        if self._sign_format.name() == SignFormats.VIDEO.value:
            self.sign_embedding_model = None
    @property
    def sign_embedding_model(self) -> Union[str, None]:
        
        if (
            self._sign_embedding_model is None
            and self.sign_format.name() != SignFormats.VIDEO.value
        ):
            raise ValueError(
                f"Sign embedding model is not set while using '{self.sign_format.name()}' sign format."
            )
        return self._sign_embedding_model
    @sign_embedding_model.setter
    def sign_embedding_model(self, model: Union[str, Enum, None]) -> None:
        if model is not None:
            if self.sign_format.name() == SignFormats.VIDEO.value:
                raise ValueError(
                    f"Can not set sign_embedding_model for {SignFormats.VIDEO.value} format because it uses raw video files."
                )
            normalized_model = normalize_short_code(model)
            if normalized_model not in SignEmbeddingModels:
                allowed = list(SignEmbeddingModels._value2member_map_.keys())
                raise ValueError(f"Invalid sign model. '{model}' not in {allowed}.")
            model = normalized_model

        elif self.sign_format.name() != SignFormats.VIDEO.value:
            raise ValueError(
                f"Sign embedding model is required for '{self.sign_format.name()}' sign_format."
            )
        self._sign_embedding_model = model
    def translate(self, text: str, *args, **kwargs) -> Sign:
        sign_language_sentence = None
        video_labels = []
        text = self.text_language.preprocess(text)
        sentences = self.text_language.sentence_tokenize(text)
        for sentence in sentences:
            tokens = self.text_language.tokenize(sentence)
            tags = self.text_language.get_tags(tokens)
            tokens, tags, contexts = self.sign_language.restructure_sentence(
                tokens, tags=tags
            )
            sign_dicts = self.sign_language.tokens_to_sign_dicts(
                tokens, tags=tags, contexts=contexts
            )
            video_labels.extend(
                [
                    label
                    for sign_dict in sign_dicts
                    for label in random.choices(
                        sign_dict[self.sign_language.SignDictKeys.SIGNS.value],
                        weights=sign_dict[self.sign_language.SignDictKeys.WEIGHTS.value], 
                        k=1,
                    )[0]
                ]
            )

        signs = self._map_labels_to_sign(video_labels)
        sign_language_sentence = self.sign_format.concatenate(signs)

        return sign_language_sentence

    def _map_labels_to_sign(self, labels: List[str]) -> List[Sign]:
        return [
            self.sign_format.load_asset(self._prepare_resource_name(label))
            for label in labels
        ]

    def _prepare_resource_name(self, label, person=None, camera=None, sep="_"):
        if person is not None:
            label = f"{label}{sep}{person}"
        if camera is not None:
            label = f"{label}{sep}{camera}"

        directory = self.sign_format.name().rstrip("s") + "s"

        extension = "unknown"
        if self.sign_format.name() == SignFormats.VIDEO.value:
            extension = "mp4"
        elif self.sign_format.name() == SignFormats.LANDMARKS.value:
            extension = "csv" 
        if self.sign_embedding_model is not None:
            extension = (
                f"{self.sign_format.name()}-{self.sign_embedding_model}.{extension}"
            )
        name = f"{directory}/{label}.{extension}"
        return name
    def __get_text_language_object(
        self, text_language: Union[str, TextLanguage, Enum]
    ) -> TextLanguage:
        if isinstance(text_language, (str, Enum)):
            return get_text_language(text_language)
        if isinstance(text_language, TextLanguage):
            return text_language
        raise TypeError(f"Expected str or TextLanguage, got {type(text_language) = }.")
    def __get_sign_language_object(
        self, sign_language: Union[str, SignLanguage, Enum]
    ) -> SignLanguage:
        if isinstance(sign_language, (str, Enum)):
            return get_sign_language(sign_language)
        if isinstance(sign_language, SignLanguage):
            return sign_language
        raise TypeError(f"Expected str or SignLanguage, got {type(sign_language) = }.")
    def __get_sign_format_class(
        self, sign_format: Union[str, Type[Sign], Enum]
    ) -> Type[Sign]:
        if isinstance(sign_format, (str, Enum)):
            return get_sign_wrapper_class(sign_format)
        if isinstance(sign_format, type) and issubclass(sign_format, Sign):
            return sign_format
        raise TypeError(f"Expected str or type[Sign], got {sign_format = }.")

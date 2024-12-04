import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'message.dart';
import 'package:chatbot/widgets/profile.dart';

class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<Message> _messages = [];

  Future<void> _sendMessage(String text) async {
    if (text.isNotEmpty) {
      setState(() {
        _messages.insert(0, Message(content: text, isUser: true));
      });

      await _sendTextMessageToApi(text);
      _controller.clear();
    }
  }

  Future<void> _sendTextMessageToApi(String text) async {
    final apiUrl = Uri.parse('http://127.0.0.1:8000/api/text_messages/');
    final response = await http.post(apiUrl, body: {'message': text});

    if (response.statusCode == 200) {
      final responseData = response.body;
      setState(() {
        _messages.insert(0, Message(content: responseData, isUser: false));
      });
    } else {
      setState(() {
        _messages.insert(0, Message(content: 'Error', isUser: false));
      });
    }
  }

  Future<void> _sendImage() async {
    final picker = ImagePicker();
    final pickedFile = await picker.getImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      final imageFile = File(pickedFile.path);
      final apiUrl = Uri.parse('http://127.0.0.1:8000/api/sign/');

      final request = http.MultipartRequest('POST', apiUrl)
        ..files.add(await http.MultipartFile.fromPath('image', imageFile.path));

      final response = await http.Response.fromStream(await request.send());

      if (response.statusCode == 200) {
        final responseData = response.body;
        setState(() {
          _messages.insert(0, Message(content: responseData, isUser: false));
        });
      } else {
        setState(() {
          _messages.insert(0, Message(content: 'Error', isUser: false));
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('ChatBot'),
        leading: IconButton(
          icon: Icon(Icons.person),
          onPressed: () {
            Navigator.push(
              context,
              _createRoute(ProfileScreen()),
            );
          },
        ),
        actions: [
          IconButton(
            icon: Icon(Icons.settings),
            onPressed: () {
              // Add settings functionality here
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              reverse: true,
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                return Align(
                  alignment: _messages[index].isUser
                      ? Alignment.centerRight
                      : Alignment.centerLeft,
                  child: Container(
                    margin: EdgeInsets.symmetric(vertical: 5, horizontal: 8),
                    padding: EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: _messages[index].isUser
                          ? Colors.blueAccent
                          : Colors.grey[300],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          _messages[index].content,
                          style: TextStyle(
                            color: _messages[index].isUser
                                ? Colors.white
                                : Colors.black,
                          ),
                        ),
                        Text(
                          _messages[index].isUser ? 'You' : 'Bot',
                          style: TextStyle(
                            fontSize: 12,
                            color: Colors.black54,
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          Divider(
            height: 1,
            color: Colors.grey,
          ),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 8.0),
            child: Row(
              children: [
                IconButton(
                  icon: Icon(Icons.photo),
                  onPressed: _sendImage,
                ),
                IconButton(
                  icon: Icon(Icons.attach_file),
                  onPressed: () {
                    // Add functionality to handle file attachment
                  },
                ),
                Expanded(
                  child: TextField(
                    controller: _controller,
                    textInputAction: TextInputAction.send,
                    onSubmitted: _sendMessage,
                    decoration: InputDecoration.collapsed(
                      hintText: 'Type a message',
                    ),
                  ),
                ),
                IconButton(
                  icon: Icon(Icons.send),
                  onPressed: () => _sendMessage(_controller.text),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Route _createRoute(Widget page) {
    return PageRouteBuilder(
      pageBuilder: (context, animation, secondaryAnimation) => page,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        const begin = Offset(1.0, 0.0);
        const end = Offset.zero;
        const curve = Curves.easeInOut;

        var tween = Tween(begin: begin, end: end).chain(CurveTween(curve: curve));
        var offsetAnimation = animation.drive(tween);

        return SlideTransition(
          position: offsetAnimation,
          child: child,
        );
      },
    );
  }
}
import 'package:flutter/material.dart';
import 'package:chatbot/widgets/login.dart';
import 'package:chatbot/widgets/signup.dart'; 
import 'package:chatbot/widgets/profile.dart'; 
import 'package:chatbot/screens/chat_screen.dart'; 
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  ); 
  runApp(ChatBot());
}
class ChatBot extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ChatBot',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      initialRoute: '/', 
      routes: {
        '/': (context) => const Login(), 
        '/signup': (context) => const SignupPage(), 
        '/profile': (context) =>  ProfileScreen(), 
        '/chat': (context) =>  ChatScreen(),
      },
    );
  }
}

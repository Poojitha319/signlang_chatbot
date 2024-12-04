import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

class SignupPage extends StatefulWidget {
  const SignupPage({super.key});

  @override
  State<SignupPage> createState() => _SignupPageState();
}

class _SignupPageState extends State<SignupPage> {
  final _auth = FirebaseAuth.instance;
  final _user = TextEditingController();
  final _pass = TextEditingController();
  final _pass1 = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  final bor = OutlineInputBorder(
      borderRadius: BorderRadius.circular(18), borderSide: BorderSide.none);

  void signup() async {
    if (_formKey.currentState!.validate()) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Register Successful'),
        ),
      );
      try {
        await _auth.createUserWithEmailAndPassword(
          email: _user.text, 
          password: _pass.text
        );
        Navigator.pop(context); // Navigate back to Login page
      } on FirebaseAuthException catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.message ?? 'Registration Failed')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Container(
          decoration: const BoxDecoration(
            image: DecorationImage(
              image: AssetImage("assets/Loki.jpg"),
              fit: BoxFit.cover,
            ),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 40),
          height: MediaQuery.of(context).size.height - 50,
          width: double.infinity,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              Column(
                children: <Widget>[
                  const SizedBox(height: 60.0),
                  const Text(
                    "Sign up",
                    style: TextStyle(
                      fontSize: 30,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(
                    height: 20,
                  ),
                  Text(
                    "Create your account",
                    style: TextStyle(fontSize: 15, color: Colors.grey[700]),
                  )
                ],
              ),
              Form(
                key: _formKey,
                child: Column(
                  children: <Widget>[
                    const SizedBox(height: 20),
                    TextFormField(
                      controller: _user,
                      validator: (value) {
                        if (value == null || !_user.text.endsWith(".com")) {
                          return 'Please enter a valid email address';
                        }
                        return null;
                      },
                      decoration: InputDecoration(
                          hintText: "Email",
                          border: bor,
                          fillColor: Colors.purple.withOpacity(0.1),
                          filled: true,
                          prefixIcon: const Icon(Icons.email)),
                    ),
                    const SizedBox(height: 20),
                    TextFormField(
                      controller: _pass,
                      validator: (value) {
                        if (value == null ||
                            value.length < 9) {
                          return 'Password must be at least 9 characters';
                        }
                        return null;
                      },
                      decoration: InputDecoration(
                        hintText: "Password",
                        border: bor,
                        fillColor: Colors.purple.withOpacity(0.1),
                        filled: true,
                        prefixIcon: const Icon(Icons.password),
                      ),
                      obscureText: true,
                    ),
                    const SizedBox(height: 20),
                    TextFormField(
                      controller: _pass1,
                      validator: (value) {
                        if (value == null || value.length < 9) {
                          return 'Password must be at least 9 characters';
                        }
                        if (value != _pass.text) {
                          return "Passwords do not match";
                        }
                        return null;
                      },
                      decoration: InputDecoration(
                        hintText: "Confirm Password",
                        border: bor,
                        fillColor: Colors.purple.withOpacity(0.1),
                        filled: true,
                        prefixIcon: const Icon(Icons.password),
                      ),
                      obscureText: true,
                    ),
                  ],
                ),
              ),
              Container(
                padding: const EdgeInsets.only(top: 3, left: 3),
                child: ElevatedButton(
                  onPressed: signup,
                  style: ElevatedButton.styleFrom(
                    shape: const StadiumBorder(),
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    backgroundColor: Colors.black,
                  ),
                  child: const Text(
                    "Sign up",
                    style: TextStyle(fontSize: 20),
                  ),
                ),
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  const Text("Already have an account?"),
                  TextButton(
                      onPressed: () {
                        Navigator.pop(context); // Navigate back to Login page
                      },
                      child: const Text(
                        "Login",
                        style: TextStyle(color: Colors.black),
                      ))
                ],
              )
            ],
          ),
        ),
      ),
    );
  }
}

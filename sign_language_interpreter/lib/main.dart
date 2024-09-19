import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:html' as html; // Use dart:html for web compatibility

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  final firstCamera = cameras.first;

  runApp(MyApp(camera: firstCamera));
}

class MyApp extends StatelessWidget {
  final CameraDescription camera;

  const MyApp({Key? key, required this.camera}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sign Language Interpreter',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(camera: camera, title: 'Sign Language Interpreter'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  final CameraDescription camera;
  final String title;

  const MyHomePage({Key? key, required this.camera, required this.title}) : super(key: key);

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  String _interpretedText = '';
  bool _isCapturing = false;

  @override
  void initState() {
    super.initState();
    _controller = CameraController(
      widget.camera,
      ResolutionPreset.high,
    );
    _initializeControllerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _sendSignLanguageData(html.File imageFile) async {
    final url = Uri.parse('http://localhost'); // Assuming backend is running locally
    try {
      final reader = html.FileReader();
      reader.readAsArrayBuffer(imageFile);
      await reader.onLoadEnd.first;

      final request = http.MultipartRequest('POST', url)
        ..files.add(http.MultipartFile.fromBytes(
          'image',
          reader.result as List<int>,
          filename: imageFile.name,
        ));
      final response = await request.send();

      if (response.statusCode == 200) {
        final responseData = await http.Response.fromStream(response);
        setState(() {
          _interpretedText = json.decode(responseData.body)['interpretedText'];
        });
      } else {
        setState(() {
          _interpretedText = 'Error: ${response.reasonPhrase}';
        });
      }
    } catch (e) {
      setState(() {
        _interpretedText = 'Error: $e';
      });
    }
  }

  Future<void> _captureAndSendImage() async {
    if (_isCapturing) return;
    setState(() {
      _isCapturing = true;
    });

    try {
      await _initializeControllerFuture;
      final image = await _controller.takePicture();
      final imageFile = html.File([await image.readAsBytes()], 'image.jpg');
      await _sendSignLanguageData(imageFile);
    } catch (e) {
      print(e);
    } finally {
      setState(() {
        _isCapturing = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: <Widget>[
              FutureBuilder<void>(
                future: _initializeControllerFuture,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.done) {
                    return AspectRatio(
                      aspectRatio: _controller.value.aspectRatio,
                      child: CameraPreview(_controller),
                    );
                  } else {
                    return const Center(child: CircularProgressIndicator());
                  }
                },
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _captureAndSendImage,
                child: const Text('Capture and Interpret'),
              ),
              const SizedBox(height: 20),
              Text(
                _interpretedText,
                style: const TextStyle(fontSize: 18),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
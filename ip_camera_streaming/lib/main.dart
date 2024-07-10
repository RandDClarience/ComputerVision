import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:easy_onvif/onvif.dart';
import 'package:loggy/loggy.dart';
import 'package:yaml/yaml.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
/*
  if (Platform.isAndroid) {
    WebViewPlatform.instance = SurfaceAndroidWebView();
  } else if (Platform.isIOS) {
    WebViewPlatform.instance = CupertinoWebView();
  }
*/
  runApp(const MaterialApp(home: CameraStream()));
}

class CameraStream extends StatefulWidget {
  const CameraStream({Key? key}) : super(key: key);

  @override
  _CameraStreamState createState() => _CameraStreamState();
}

class _CameraStreamState extends State<CameraStream> {
  final Completer<WebViewController> _controller =
      Completer<WebViewController>();
  String? streamUri;

  @override
  void initState() {
    super.initState();
    _initializeOnvif();
  }

  Future<void> _initializeOnvif() async {
    try {
      final config = loadYaml(File('config.yaml').readAsStringSync());

      final onvif = await Onvif.connect(
        host: config['host'],
        username: config['username'],
        password: config['password'],
        logOptions: const LogOptions(
          LogLevel.debug,
          stackTraceLevel: LogLevel.error,
        ),
        printer: const PrettyPrinter(
          showColors: true,
        ),
      );

      var profiles = await onvif.media.getProfiles();
      var mediaUri = await onvif.media.getStreamUri(profiles[0].token);

      setState(() {
        streamUri = mediaUri.uri; // Extract the URI string
      });
    } catch (e) {
      print("Error: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('IP Camera Stream'),
      ),
      body: streamUri == null
          ? const Center(child: CircularProgressIndicator())
          : WebView(
              initialUrl: streamUri,
              javascriptMode: JavascriptMode.unrestricted,
              onWebViewCreated: (WebViewController webViewController) {
                _controller.complete(webViewController);
              },
              onPageStarted: (String url) {
                print('Page started loading: $url');
              },
              onPageFinished: (String url) {
                print('Page finished loading: $url');
              },
            ),
    );
  }
}

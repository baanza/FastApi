import 'package:web_socket_channel/web_socket_channel.dart';

void main(List<String> arguments){
  final channel = WebSocketChannel.connect(
    Uri.parse("ws://127.0.0.1:8000/ws")
  );

  channel.stream.listen((data){
    print(data);
  },
  onError: (error) => print(error),
  );
}
---
name : 'Pipecat transport configurations'
filename : 'pipecat_transport_configurations.md'
description : 'Comprehensive research on Pipecat transport layer configurations, including setup procedures, implementation details, and best practices for WebRTC and WebSocket transports'
key_points : ["DailyTransport WebRTC setup", "LiveKitTransport configuration", "SmallWebRTCTransport peer-to-peer", "TransportParams audio/video settings", "Environment variables configuration", "Multi-transport type detection", "Client-side JavaScript setup", "Production deployment strategies", "Error handling and resource management", "Security best practices"]
---

# Pipecat Transport Configurations - Comprehensive Research

## Overview

Pipecat is an open-source framework for building voice and multimodal conversational AI applications. A critical component of Pipecat is its transport layer, which handles real-time communication between users and AI agents. This research document provides comprehensive knowledge about Pipecat transport configurations, focusing on implementation details, setup procedures, and best practices.

## Supported Transport Types

Pipecat supports multiple transport protocols, each suited for different use cases:

### 1. DailyTransport (WebRTC)
- **Provider**: Daily.co
- **Protocol**: WebRTC
- **Use Case**: Production-ready voice/video calls with hosted infrastructure
- **Key Features**: Global infrastructure, low-latency streaming, multi-participant support, built-in transcription

### 2. LiveKitTransport (WebRTC)
- **Provider**: LiveKit
- **Protocol**: WebRTC
- **Use Case**: Open-source real-time communication platform
- **Key Features**: Self-hosted or cloud options, data channels, room management

### 3. SmallWebRTCTransport (WebRTC)
- **Provider**: Peer-to-peer
- **Protocol**: WebRTC
- **Use Case**: Direct peer-to-peer connections, local development, demos
- **Key Features**: No third-party infrastructure required, lightweight

### 4. WebSocket Transports
- **Protocol**: WebSocket
- **Use Case**: Custom implementations, telephony integration
- **Key Features**: Flexible frame serialization, reconnection strategies

## Installation Requirements

### DailyTransport
```bash
pip install "pipecat-ai[daily]"
```

### LiveKitTransport
```bash
pip install "pipecat-ai[livekit]"
```

### Client-side JavaScript/TypeScript
```bash
npm install @pipecat-ai/client-js
npm install @pipecat-ai/daily-transport
# or
npm install @pipecat-ai/small-webrtc-transport
```

## Configuration Details

### Environment Variables

#### DailyTransport
- `DAILY_API_KEY`: Required for Daily API authentication
- `DAILY_API_URL`: Optional custom Daily API URL

#### LiveKitTransport
- `LIVEKIT_API_KEY`: Required for LiveKit API authentication
- `LIVEKIT_API_SECRET`: Required for LiveKit API secret
- `LIVEKIT_URL`: Required for LiveKit server URL
- `LIVEKIT_ROOM_NAME`: Optional default room name

### TransportParams Configuration

The base `TransportParams` class provides common configuration options across all transport types:

#### Audio Settings
```python
TransportParams(
    audio_in_enabled=True,      # Enable audio input
    audio_out_enabled=True,     # Enable audio output
    audio_in_sample_rate=16000,  # Input sample rate
    audio_out_sample_rate=16000, # Output sample rate
    audio_in_channels=1,         # Input channels
    audio_out_channels=1,        # Output channels
)
```

#### Video Settings
```python
TransportParams(
    video_in_enabled=True,       # Enable video input
    video_out_enabled=True,      # Enable video output
    video_out_width=1280,        # Output width
    video_out_height=720,        # Output height
    video_out_bitrate=1000000,  # Output bitrate
    video_out_framerate=30,      # Output framerate
)
```

#### Voice Activity Detection (VAD)
```python
TransportParams(
    vad_analyzer=SileroVADAnalyzer(),  # VAD implementation
)
```

#### Turn Detection
```python
TransportParams(
    turn_analyzer=SmartTurnDetection(), # Conversation turn management
)
```

## Implementation Examples

### Python Server-side Configuration

#### DailyTransport Basic Setup
```python
from pipecat.transports.services.daily import DailyTransport, DailyParams

async def bot(runner_args):
    transport = DailyTransport(
        room_url=runner_args.room_url,
        token=runner_args.token,
        bot_name="AI Assistant",
        params=DailyParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            vad_analyzer=SileroVADAnalyzer(),
        )
    )
    await run_pipeline(transport)
```

#### LiveKitTransport Basic Setup
```python
from pipecat.transports.services.livekit import LiveKitTransport, LiveKitParams

async def bot(runner_args):
    transport = LiveKitTransport(
        url=runner_args.url,
        token=runner_args.token,
        room_name=runner_args.room_name,
        bot_name="AI Assistant",
        params=LiveKitParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            vad_analyzer=SileroVADAnalyzer(),
        )
    )
    await run_pipeline(transport)
```

#### SmallWebRTCTransport Setup
```python
from pipecat.transports.small_webrtc import SmallWebRTCTransport

async def bot(runner_args):
    transport = SmallWebRTCTransport(
        params=TransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            vad_analyzer=SileroVADAnalyzer(),
        ),
        webrtc_connection=runner_args.webrtc_connection,
    )
    await run_pipeline(transport)
```

### Transport Utilities Configuration

#### Daily Configuration with Utilities
```python
from pipecat.runner.utils.configure import configure

async def setup_daily_transport(session):
    room_config = await configure(session)
    transport = DailyTransport(
        room_url=room_config.room_url,
        token=room_config.token,
        bot_name="AI Assistant",
        params=DailyParams()
    )
    return transport
```

#### LiveKit Configuration with Utilities
```python
from pipecat.runner.utils.configure import configure

async def setup_livekit_transport(session):
    config = await configure(session)
    transport = LiveKitTransport(
        url=config.url,
        token=config.token,
        room_name=config.room_name,
        bot_name="AI Assistant",
        params=LiveKitParams()
    )
    return transport
```

### Client-side JavaScript Configuration

#### DailyTransport Client Setup
```javascript
import { PipecatClient } from "@pipecat-ai/client-js";
import { DailyTransport } from "@pipecat-ai/daily-transport";

const pcClient = new PipecatClient({
    transport: new DailyTransport({
        bufferLocalAudioUntilBotReady: true,
        // Additional DailyTransport options
    }),
    enableMic: true,
    callbacks: {
        onTrackStarted: handleBotAudio,
    },
});

pcClient.connect({ url: "YOUR_DAILY_URL" });
```

#### SmallWebRTCTransport Client Setup
```javascript
import { PipecatClient } from "@pipecat-ai/client-js";
import { SmallWebRTCTransport } from "@pipecat-ai/small-webrtc-transport";

const pcClient = new PipecatClient({
    transport: new SmallWebRTCTransport({
        iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
        waitForICEGathering: true,
        webrtcUrl: "YOUR_WEBRTC_SIGNALING_URL",
        audioCodec: "opus",
        videoCodec: "vp8",
    }),
    enableMic: true,
    callbacks: {
        onTrackStarted: handleBotAudio,
    },
});
```

## Advanced Configuration Options

### DailyParams Specific Options
```python
DailyParams(
    api_url="https://api.daily.co/v1",  # Daily API URL
    api_key="your-api-key",             # Daily API key
    transcription_enabled=True,         # Enable transcription
    transcription_settings=DailyTranscriptionSettings(
        provider="deepgram",
        language="en-US",
    ),
    dialin_settings=DailyDialinSettings(
        call_id="call-123",
        call_domain="domain.daily.co",
    ),
    camera_out_enabled=True,            # Enable camera output
    microphone_out_enabled=True,         # Enable microphone output
)
```

### LiveKitParams Specific Options
```python
LiveKitParams(
    # Inherits all TransportParams options
    # LiveKit-specific configurations are handled through token generation
)
```

### WebSocket Transport Configuration
```python
from pipecat.transports.websocket import FastAPIWebsocketTransport

transport = FastAPIWebsocketTransport(
    params=FastAPIWebsocketParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        sample_rate=16000,
        channels=1,
        # Custom frame serialization
        frame_serializer=CustomFrameSerializer(),
        # Reconnection strategy
        max_reconnect_attempts=5,
        reconnect_delay=1.0,
    )
)
```

## Multi-Transport Support

Pipecat supports type-safe detection and handling of multiple transport types:

```python
async def bot(runner_args):
    # Type-safe transport detection
    if isinstance(runner_args, DailyRunnerArguments):
        transport = DailyTransport(
            runner_args.room_url,
            runner_args.token,
            "Bot",
            DailyParams(...)
        )
    elif isinstance(runner_args, LiveKitRunnerArguments):
        transport = LiveKitTransport(
            runner_args.url,
            runner_args.token,
            runner_args.room_name,
            "Bot",
            LiveKitParams(...)
        )
    elif isinstance(runner_args, WebsocketRunnerArguments):
        transport = FastAPIWebsocketTransport(
            websocket=runner_args.websocket,
            params=FastAPIWebsocketParams(...)
        )
    
    await run_pipeline(transport)
```

## Best Practices

### 1. Transport Selection
- **DailyTransport**: Use for production applications requiring reliable WebRTC infrastructure
- **LiveKitTransport**: Use when open-source infrastructure or self-hosting is preferred
- **SmallWebRTCTransport**: Use for local development, testing, and simple demos
- **WebSocket**: Use for custom protocols or telephony integration

### 2. Error Handling
```python
try:
    await run_pipeline(transport)
except TransportError as e:
    logger.error(f"Transport error: {e}")
    # Implement reconnection logic
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Cleanup and exit
```

### 3. Resource Management
```python
async def bot(runner_args):
    transport = DailyTransport(...)
    try:
        await run_pipeline(transport)
    finally:
        await transport.cleanup()  # Ensure proper cleanup
```

### 4. Security Considerations
- Store API keys in environment variables, not in code
- Use HTTPS/WSS for all connections
- Implement proper authentication and authorization
- Validate all input parameters

## Development and Testing

### Local Development Setup
1. Install required dependencies for your chosen transport
2. Set up environment variables
3. Use the development runner for testing:
```bash
python -m pipecat.runner.run --use-daily
# or
python -m pipecat.runner.run --use-livekit
```

### Testing Strategies
- Unit test transport configuration
- Integration test with actual transport services
- Load test for concurrent connections
- Network condition testing (latency, packet loss)

## Production Deployment

### Pipecat Cloud Integration
- Integrated Daily API key with zero configuration
- Free voice minutes for 1:1 calls
- Simplified deployment with `--use-daily` flag

### Custom Deployment
- Use your own Daily/LiveKit API keys
- Configure according to your infrastructure
- Monitor usage and costs

### Infrastructure Considerations
- Choose appropriate transport for your scale
- Implement proper monitoring and logging
- Set up alerting for transport failures
- Plan for horizontal scaling

## Troubleshooting

### Common Issues
1. **Connection Failures**: Check API keys and network connectivity
2. **Audio Issues**: Verify sample rates and channel configurations
3. **Video Problems**: Ensure codec compatibility and bandwidth
4. **Performance**: Optimize VAD settings and reduce latency

### Debug Tools
- Pipecat logging with transport-specific details
- Daily/LiveKit dashboard monitoring
- Network analysis tools
- Audio/video quality metrics

## Conclusion

Pipecat's transport layer provides flexible and robust options for real-time communication in voice AI applications. The choice of transport depends on specific requirements such as infrastructure preferences, scalability needs, and development complexity. DailyTransport offers the most straightforward path to production, while LiveKitTransport provides open-source flexibility, and SmallWebRTCTransport enables simple peer-to-peer scenarios.

Proper configuration of TransportParams, environment variables, and transport-specific settings ensures optimal performance and reliability. The framework's type-safe multi-transport support allows for flexible deployment strategies across different use cases and environments.

## References

- [Pipecat Documentation](https://docs.pipecat.ai)
- [Pipecat Examples Repository](https://github.com/pipecat-ai/pipecat-examples)
- [Daily.co Documentation](https://docs.daily.co)
- [LiveKit Documentation](https://docs.livekit.io)

# QGroundControl Listener and MAVLink Forwarder

This project contains a Python script that acts as a UDP-based **MAVLink message forwarder and decoder** between **QGroundControl (QGC)** and **ArduPilot SITL**. It forwards traffic bidirectionally and logs **mission-related messages** sent by QGC, enabling analysis and reverse engineering of how QGC defines and starts missions.

---

## ✨ Features

- Forwards MAVLink traffic **from QGC to SITL** and **from SITL to QGC**
- **Decodes and logs** QGC messages like `MISSION_ITEM_INT`, `COMMAND_LONG`, and more
- **Filters out** irrelevant messages (e.g., `HEARTBEAT`, `REQUEST_DATA_STREAM`)
- Learns source and destination addresses dynamically (no hardcoded QGC/SITL ports)
- Helps reverse engineer MAVLink-based mission workflows

---

## 🔧 Requirements

- Python 3
- [pymavlink](https://github.com/ArduPilot/pymavlink)

Install dependencies using pip:

```bash
pip install pymavlink
```

---

## 🔧 Usage

### Run the Listener

```bash
python "MAVSniff.py"
```

The script will:
- Bind to port `14560` to receive messages from QGC
- Bind to port `14551` to receive messages from SITL
- Forward traffic in both directions
- Decode and log only **QGC → SITL mission-related messages**

---

## 🛋️ How It Works

This script:
- Uses UDP sockets for two-way MAVLink communication
- Uses `pymavlink` to decode messages from QGC
- Tracks and forwards MAVLink messages in real time
- Dynamically learns the IP and port of both QGC and SITL to route traffic
- Filters out `HEARTBEAT` and `REQUEST_DATA_STREAM` to focus on mission logic

---

## 🌎 Setting Up QGC and SITL

### QGroundControl Setup

In **QGC**, go to:

**Settings → Comm Links → Add**:

- Name: `To Listener`
- Type: `UDP`
- Target Host: `127.0.0.1`
- Target Port: `14560`
- Listening Port: Leave blank or use something unused (e.g., `14561`)

Click **Connect**.

### SITL Setup

Start ArduPlane SITL with the following options:

```bash
sim_vehicle.py -v ArduPlane --console --map --out=udp:127.0.0.1:14551
```

This sends MAVLink messages to the listener on port `14551`.

---

## 📊 Example Output

When you upload and start a mission in QGC, you will see decoded messages like:

```
[QGC → SITL] MAVLink message received:
  Type: MISSION_COUNT
  Fields: {'count': 10, 'target_system': 1, ...}

[QGC → SITL] MAVLink message received:
  Type: MISSION_ITEM_INT
  Fields: {'seq': 0, 'command': 16, 'x': 370436560, 'y': 353917552, 'z': 30.0, ...}

[QGC → SITL] MAVLink message received:
  Type: COMMAND_LONG
  Fields: {'command': 400, 'param1': 1.0, ...}  # Arm command
```

This helps you track the exact sequence of commands used to define and execute a mission.

---

## ❌ Filtered-Out Messages

To focus only on mission-relevant messages, the script ignores:

- `HEARTBEAT`: sent regularly by QGC and SITL
- `REQUEST_DATA_STREAM`: legacy message requesting telemetry streams

You can customize this filter in the script.

---

---

## 🔺 Why Use This Script?

This listener lets you:
- Understand how QGC structures missions
- Replay command sequences using `pymavlink`
- Monitor and debug MAVLink ground-to-autopilot communication

This is ideal for building **custom GCS**, **AI autopilots**, or **MAVLink test tools**.

---

## 📖 License

MIT License. Use, modify, and distribute freely.

---

## 🚀 Next Steps

- Add logging to file or CSV
- Build a mission replayer using captured messages
- Visualize GPS waypoints using `matplotlib` or `folium`
- Extend to support multiple vehicles or components

Let us know if you'd like help with any of these extensions!

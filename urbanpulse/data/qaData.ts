export interface SupportingDoc {
  title: string;
  url: string;
}

export interface QAItem {
  id: number;
  question: string;
  answer: string;
  documents: SupportingDoc[];
  category: string;
}

export const QA_DATA: QAItem[] = [
  // ── Networking and Offline Resilience ─────────────────────────────────────
  {
    id: 1,
    category: "Networking",
    question: "Why Wi-Fi Aware instead of Bluetooth or BLE?",
    answer:
      "BLE is excellent for discovery and very small packets, but our urban-event packets may include metadata and selected evidence images. Wi-Fi Aware allows nearby Android devices to discover each other and establish direct peer-to-peer network connections without an access point, and Android documents that these connections can offer higher throughput and longer distance than Bluetooth.",
    documents: [
      {
        title: "Android Developers – Wi-Fi Aware overview",
        url: "https://developer.android.com/develop/connectivity/wifi/wifi-aware",
      },
    ],
  },
  {
    id: 2,
    category: "Networking",
    question: "What happens when a bus has no internet?",
    answer:
      "The event is processed by Edge AI and stored locally. When the bus encounters another compatible node, the event can be forwarded. Eventually, a node with internet connectivity uploads it to the central platform. This is our store-carry-forward mechanism.",
    documents: [
      {
        title: "IETF RFC 9171 – Bundle Protocol Version 7",
        url: "https://www.rfc-editor.org/rfc/rfc9171.html",
      },
    ],
  },
  {
    id: 6,
    category: "Networking",
    question: "Suppose there are no nearby buses and no internet. What happens?",
    answer:
      "The event remains safely stored on the originating bus. The bus physically carries the information until internet connectivity returns or another peer becomes available, after which the event can be forwarded.",
    documents: [
      {
        title: "IETF RFC 9171 – Delay-Tolerant Networking / Bundle Protocol",
        url: "https://www.rfc-editor.org/rfc/rfc9171.html",
      },
    ],
  },
  {
    id: 7,
    category: "Networking",
    question:
      "What distance between two buses is required for mesh data transmission?",
    answer:
      "There is no minimum separation requirement; the important value is the maximum reliable communication range. For our prototype and SUMO simulation we use a conservative 30–50 m peer-eligibility threshold. In deployment, we would calibrate this using the actual hardware, signal conditions, and supported ranging rather than treating 50 m as a guaranteed Wi-Fi Aware limit. Note: the 30–50 m value is a configurable simulation parameter, not an official fixed Wi-Fi Aware range.",
    documents: [
      {
        title: "Android Developers – Wi-Fi Aware overview",
        url: "https://developer.android.com/develop/connectivity/wifi/wifi-aware",
      },
      {
        title: "Android Developers – Wi-Fi RTT ranging",
        url: "https://developer.android.com/develop/connectivity/wifi/wifi-rtt",
      },
    ],
  },

  // ── AI, Video and Event Intelligence ──────────────────────────────────────
  {
    id: 3,
    category: "AI & Vision",
    question: "Which AI model are you using?",
    answer:
      "For the prototype, we use Ultralytics YOLO for real-time object and event detection because it provides a strong balance between inference speed and detection capability. OpenCV handles camera/video capture, frame processing, preprocessing, and related image operations.",
    documents: [
      {
        title: "Ultralytics – Object Detection with YOLO",
        url: "https://docs.ultralytics.com/tasks/detect/",
      },
      {
        title: "OpenCV – VideoCapture class reference",
        url: "https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html",
      },
    ],
  },
  {
    id: 4,
    category: "AI & Vision",
    question:
      "Are you sending all camera feeds to the cloud for AI processing?",
    answer:
      "No. The primary detection runs at the edge. Only meaningful events and selected evidence need to be transmitted. This reduces bandwidth, latency, and unnecessary cloud processing. The SIH26124 expected solution itself calls for onboard edge-AI processing while minimising bandwidth through intelligent edge processing.",
    documents: [
      {
        title: "SIH26124 problem statement – community archive",
        url: "https://sih2026.vuce.in/ps/SIH26124",
      },
    ],
  },
  {
    id: 12,
    category: "AI & Vision",
    question:
      "How confident is your system after detecting a pothole or urban incident?",
    answer:
      "We do not rely on a single score alone. YOLO provides a per-detection confidence score, and our application can combine it with repeated-frame consistency, location consistency, and confirmation from other sensing nodes. The purpose of peer verification is to reduce reliance on a single observation before an important event is treated as verified.",
    documents: [
      {
        title: "Ultralytics – Detection confidence scores",
        url: "https://docs.ultralytics.com/tasks/detect/",
      },
      {
        title: "Sensors – Cooperative Perception Technology Review",
        url: "https://www.mdpi.com/1424-8220/22/15/5535",
      },
    ],
  },
  {
    id: 13,
    category: "AI & Vision",
    question:
      "Is your AI model only analysing pre-recorded videos, or can it analyse live video in real time?",
    answer:
      "It can do both. For testing, we can use recorded or simulated video. The same pipeline is designed to consume live camera streams from bus dashcams or CCTV. OpenCV VideoCapture supports cameras, files, and video streams, while YOLO supports object detection on image and video inputs.",
    documents: [
      {
        title: "OpenCV – VideoCapture class reference",
        url: "https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html",
      },
      {
        title: "Ultralytics – YOLO documentation",
        url: "https://docs.ultralytics.com/",
      },
    ],
  },
  {
    id: 14,
    category: "AI & Vision",
    question:
      "Why are you using both YOLO and OpenCV? Aren't both computer vision models?",
    answer:
      "OpenCV is not the AI detection model in our pipeline. OpenCV handles video acquisition and image processing operations, while YOLO performs the learned object detection. In simple terms: OpenCV processes the video pipeline; YOLO identifies objects and events in the frames.",
    documents: [
      {
        title: "OpenCV – VideoCapture class reference",
        url: "https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html",
      },
      {
        title: "Ultralytics – Object Detection with YOLO",
        url: "https://docs.ultralytics.com/tasks/detect/",
      },
    ],
  },

  // ── Hardware, Cost and Bus-Side Operation ─────────────────────────────────
  {
    id: 5,
    category: "Hardware",
    question: "Do buses require expensive new hardware?",
    answer:
      "Not necessarily for the prototype. We can demonstrate the solution using existing cameras, Android devices or edge computers, GPS, and available connectivity. A production deployment can move to dedicated rugged edge hardware if required by the transport authority.",
    documents: [
      {
        title: "SIH26124 problem statement – community archive",
        url: "https://sih2026.vuce.in/ps/SIH26124",
      },
      {
        title: "Raspberry Pi 5 – official product specifications",
        url: "https://www.raspberrypi.com/products/raspberry-pi-5/",
      },
    ],
  },
  {
    id: 8,
    category: "Hardware",
    question:
      "What if one of the buses itself gets into an accident? How will the system recognise it?",
    answer:
      "We do not rely only on the camera. A possible bus accident can be detected by combining IMU motion data, sudden speed change, GPS or vehicle telemetry, and camera evidence. If multiple signals agree, the event becomes a high-priority emergency and can be propagated through the available network path.",
    documents: [
      {
        title:
          "Electronics (MDPI) – Road Accidents Detection using V2X, edge/cloud, accelerometer, gyroscope, GPS and camera",
        url: "https://www.mdpi.com/2079-9292/8/8/896",
      },
    ],
  },
  {
    id: 9,
    category: "Hardware",
    question: "Why Raspberry Pi when there are edge devices such as ESP32?",
    answer:
      "Raspberry Pi is used because our vision workload includes YOLO, OpenCV, OCR, and live video processing. ESP32-class microcontrollers are better suited to lightweight sensing, telemetry, IMU, GPS, and embedded control. In our architecture, the ESP32 can handle low-power sensor tasks while Raspberry Pi or Jetson handles the heavier vision AI workload.",
    documents: [
      {
        title: "Espressif – ESP32-S3 official specifications",
        url: "https://www.espressif.com/en/products/socs/esp32s3/docs",
      },
      {
        title: "Raspberry Pi 5 – official specifications",
        url: "https://www.raspberrypi.com/products/raspberry-pi-5/",
      },
    ],
  },
  {
    id: 10,
    category: "Hardware",
    question: "Won't installing dashcams on every bus make the solution expensive?",
    answer:
      "The BEL problem statement already assumes that modern buses are increasingly equipped with multiple onboard cameras. Our approach is to utilise those existing dashcams and onboard cameras more effectively by adding Edge AI and analytics rather than treating every bus as a completely new camera installation. Note: the cited page is a community-maintained archive of the SIH problem statement and explicitly identifies itself as unofficial.",
    documents: [
      {
        title:
          "SIH26124 – AI-Powered Mobile Urban Intelligence Platform Using Public Transport Fleet",
        url: "https://sih2026.vuce.in/ps/SIH26124",
      },
    ],
  },
  {
    id: 11,
    category: "Hardware",
    question: "Won't this increase infrastructure costs for the city?",
    answer:
      "Our goal is to reuse existing public-transport and CCTV infrastructure and add intelligence on top of it. Because buses already travel through the city and existing cameras already capture video, the solution can extend sensing coverage without requiring a new fixed camera installation on every road.",
    documents: [
      {
        title: "SIH26124 problem statement – community archive",
        url: "https://sih2026.vuce.in/ps/SIH26124",
      },
    ],
  },
  {
    id: 17,
    category: "Hardware",
    question:
      "How do ESP32, Raspberry Pi and NVIDIA Jetson compare for this project?",
    answer:
      "We choose hardware based on workload. ESP32-S3 is suitable for lightweight sensing and telemetry; Raspberry Pi 5 is a cost-effective Linux edge computer for the prototype; Jetson Orin Nano is the stronger option for heavier real-time AI workloads because it is purpose-built for edge AI acceleration.",
    documents: [
      {
        title: "Espressif – ESP32-S3 official specifications",
        url: "https://www.espressif.com/en/products/socs/esp32s3/docs",
      },
      {
        title: "Raspberry Pi 5 – official specifications",
        url: "https://www.raspberrypi.com/products/raspberry-pi-5/",
      },
      {
        title: "NVIDIA – Jetson module lineup and Orin Nano specifications",
        url: "https://developer.nvidia.com/embedded/jetson-modules",
      },
    ],
  },
  {
    id: 18,
    category: "Hardware",
    question: "What is the expected energy consumption of the AI system?",
    answer:
      "The AI model itself does not have one fixed wattage; power depends on the edge hardware, camera count, model size, inference rate, and workload. Raspberry Pi states that Pi 5 can peak at around 12 W under very intensive board workloads. NVIDIA documents Jetson Orin Nano power modes ranging from 7 W to 25 W depending on model and configuration. We can reduce average consumption through lightweight models, optimised inference, and selective frame processing.",
    documents: [
      {
        title: "Raspberry Pi – Introducing Raspberry Pi 5 (power discussion)",
        url: "https://www.raspberrypi.com/news/introducing-raspberry-pi-5/",
      },
      {
        title: "NVIDIA – Jetson Orin Nano power modes",
        url: "https://docs.nvidia.com/jetson/archives/r36.5/DeveloperGuide/SD/PlatformPowerAndPerformance/JetsonOrinNanoSeriesJetsonOrinNxSeriesAndJetsonAgxOrinSeries.html",
      },
    ],
  },

  // ── Simulation and System Validation ──────────────────────────────────────
  {
    id: 15,
    category: "Simulation",
    question: "Why are you using both Webots and SUMO for simulation?",
    answer:
      "They simulate different layers. Webots provides the physical 3D environment, vehicle sensors, and camera simulation, while SUMO handles large-scale traffic flow, routes, signals, and multi-vehicle traffic logic. Webots officially provides a SUMO interface that uses TraCI to synchronise the two simulators.",
    documents: [
      {
        title: "Cyberbotics Webots – SUMO Interface",
        url: "https://cyberbotics.com/doc/automobile/sumo-interface?tab-language=c&version=released",
      },
      {
        title: "SUMO – Official user documentation",
        url: "https://sumo.dlr.de/docs/",
      },
    ],
  },

  // ── Security and Trust ─────────────────────────────────────────────────────
  {
    id: 16,
    category: "Security",
    question:
      "What security measures are you using to protect the system and prevent fake or tampered data?",
    answer:
      "We protect the system in layers: authenticated device identities, encrypted communication, signed or integrity-protected event packets, role-based dashboard access, secure local/cloud storage, replay protection using event IDs and timestamps, and audit logs. A production design should follow zero-trust principles so a node is not trusted simply because it is physically nearby or connected to the same network.",
    documents: [
      {
        title: "NIST SP 800-207 – Zero Trust Architecture",
        url: "https://csrc.nist.gov/pubs/sp/800/207/final",
      },
      {
        title: "IETF RFC 8446 – TLS 1.3",
        url: "https://www.rfc-editor.org/rfc/rfc8446.html",
      },
      {
        title: "Espressif – ESP32-S3 security features",
        url: "https://www.espressif.com/en/products/socs/esp32s3/docs",
      },
    ],
  },
];

export const CATEGORIES = [
  "All",
  "Networking",
  "AI & Vision",
  "Hardware",
  "Simulation",
  "Security",
] as const;

export type Category = (typeof CATEGORIES)[number];

# 🤖 ROS 2 → ABB IRB 1200 MoveIt Bridge (RWS + RAPID)

Bu proje, ROS 2 MoveIt tarafından planlanan robot yörüngelerini yakalayıp ABB Robot Web Services (RWS) üzerinden **ABB IRB 1200** robotuna ileten hafif bir köprü sistemidir.

Sistem, ROS 2’nin hareket planlama altyapısını ABB’nin endüstriyel kontrol sistemi ile gerçek zamanlıya yakın şekilde entegre eder.

---

## 🧠 Desteklenen Robot

* ABB IRB 1200 (Gen 2 dahil)

Özellikler:

* 5–9 kg payload seçenekleri
* 0.7 m / 0.9 m reach varyantları
* Yüksek hız ve hassasiyet (≈0.01 mm repeatability)
* OmniCore kontrolcü uyumlu

---

## 🏗 Sistem Mimarisi

```
MoveIt (ROS 2)
     │
     ▼
/display_planned_path topic
     │
     ▼
moveit_to_abb.py (ROS 2 Node)
     │
     ├── Radyan → Derece dönüşümü
     ├── Joint trajectory parse
     ▼
ABB Robot Web Services (RWS)
     │
     ▼
ABB RAPID (ROS_Bridge modülü)
     │
     ▼
MoveAbsJ
     │
     ▼
IRB 1200 robot hareketi
```

---

## 📦 Proje İçeriği

```
/moveit_to_abb.py        → ROS 2 bridge node
/ROS_Bridge_RAPID.mod    → ABB RAPID programı
```

---

## ⚙️ Gereksinimler

### 🖥 Sistem

* Ubuntu 24.04 LTS
* ROS 2 Jazzy
* MoveIt 2

### 🤖 ROS Paketleri

```bash
sudo apt install ros-$ROS_DISTRO-moveit-msgs
sudo apt install ros-$ROS_DISTRO-abb-robot-client
```

### 🐍 Python bağımlılıkları

```bash
pip install requests numpy
```

---

## 🚀 Kurulum

### 1. ROS 2 workspace oluştur

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

git clone <repo-url>
cd ..
colcon build
source install/setup.bash
```

---

## 🤖 ABB Robot (RAPID Setup)

RobotStudio veya gerçek kontrolcüye şu RAPID modülü yüklenir:

### 🔁 RAPID Program (ROS_Bridge)

* Sürekli döngüde çalışır
* `move_flag` sinyali bekler
* Gelen joint hedefini `MoveAbsJ` ile uygular

```rapid
MODULE ROS_Bridge

PERS bool move_flag := FALSE;
PERS jointtarget target_pose;

PROC main()
    WHILE TRUE DO

        IF move_flag THEN
            MoveAbsJ target_pose, v100, fine, tool0;
            move_flag := FALSE;
        ENDIF

        WaitTime 0.01;

    ENDWHILE
ENDPROC

ENDMODULE
```

---

## 🌐 RWS Bağlantısı

ROS tarafında robot IP ayarlanır:

```bash
ros2 run abb_rws_client rws_client --ros-args \
  -p robot_ip:="192.168.125.1" \
  -p robot_port:=80 \
  -r /rws/joint_states:=/joint_states
```

---

## 🧩 ROS Node (moveit_to_abb.py)

Görevleri:

* `/display_planned_path` dinler
* Joint trajectory alır
* Radyan → derece çevirir
* ABB formatına çevirip RWS’ye gönderir

---

## ⚠️ Bilinen Limitler

* Sadece **joint-space hareket**
* Cartesian path desteklenmez
* Trajectory “streaming” değil, snapshot mantığıyla gönderilir
* Feedback (geri bildirim) yok
* Collision avoidance ABB tarafına bırakılmıştır

---

## 🔧 MoveIt Başlatma

Örnek:

```bash
ros2 launch irb1200_moveit_config demo.launch.py
```

---

## 🧪 Test Akışı

1. ABB RAPID programını başlat
2. RWS client’ı çalıştır
3. MoveIt’ten plan oluştur
4. `/display_planned_path` yayınlanır
5. Robot hareket eder

---

## 📊 Geliştirme Notları

* IRB 1200 RWS gecikmesi ~50–150 ms olabilir
* Trajectory smoothing önerilir
* Joint limit kontrolü ROS tarafında yapılmalı

---

## 📌 Gelecek Geliştirmeler

* Cartesian path desteği
* Real-time streaming (EGM benzeri)
* Feedback loop (joint state sync)
* Velocity scaling control
* Safety zone integration

---

## 📄 Lisans

MIT License

---

## 🔥 Özet

Bu proje:

* MoveIt planlarını alır
* ABB IRB 1200’e gönderir
* RAPID üzerinden çalıştırır

---

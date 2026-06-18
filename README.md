# ROS 2 MoveIt to ABB Robot Bridge via RWS

Bu proje, ROS 2 MoveIt tarafından planlanan yörüngeleri (trajectory) anlık olarak yakalayan ve ABB Robot Web Services (RWS) üzerinden gerçek veya simüle edilmiş bir ABB robot koluna ileten hafif ve etkili bir köprü (bridge) uygulamasıdır.

## 🛠️ Sistem Mimarisi

Sistem iki temel bileşenden oluşmaktadır:
1. **ROS 2 Düğümü (`moveit_to_abb.py`)**: MoveIt'in `/display_planned_path` konusunu dinler, radyan cinsinden gelen eklem açılarını dereceye çevirir ve RWS servisleri aracılığıyla robota gönderir.
2. **RAPID Modülü (`ROS_Bridge`)**: ABB tarafında çalışan, gelen `move_flag` sinyalini bekleyen ve `MoveAbsJ` komutu ile robotu hedef konuma süren sonsuz döngü programı.

---

## 📂 Proje İçeriği

* `moveit_to_abb.py` - ROS 2 MoveIt planlama köprü betiği.
* `ROS_Bridge_RAPID.txt` - ABB Kontrolcüsü için yazılmış RAPID kaynak kodu.

---

## 🚀 Çalıştırma Talimatları

Projenin eksiksiz çalışabilmesi için aşağıdaki adımları sırasıyla farklı terminallerde uygulayınız:

### 1. ABB Kontrolcü Tarafı (RAPID)
`ROS_Bridge_RAPID.txt` içerisindeki kodu RobotStudio veya FlexPendant kullanarak robotunuza yükleyin. PP to Main yaptıktan sonra sistemi **START** konumuna getirin. Robot döngüye girip sinyal beklemeye başlayacaktır.

### 2. ROS 2 RWS İstemcisi
Robot ile ROS 2 ağı arasındaki temel haberleşmeyi başlatmak için ilk terminalde şu komutu çalıştırın:
```bash
ros2 run abb_rws_client rws_client --ros-args \
    -p robot_ip:="192.168.125.1" \
    -p robot_port:=80 \
    -p no_connection_timeout:=false \
    -r /rws/joint_states:=/joint_states

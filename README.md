# ROS 2 MoveIt to ABB Robot Bridge via RWS

Bu proje, ROS 2 MoveIt tarafından planlanan yörüngeleri (*trajectory*) anlık olarak yakalayan ve ABB Robot Web Services (RWS) üzerinden gerçek veya simüle edilmiş bir ABB robot koluna ileten hafif ve etkili bir köprü (*bridge*) uygulamasıdır.

Sistem, ROS 2'nin gelişmiş hareket planlama kabiliyetleri ile ABB'nin endüstriyel kontrolcü altyapısını minimum gecikmeyle birbirine bağlamayı amaçlar.

---

## 🛠️ Sistem Mimarisi

Sistem iki temel bileşenden oluşmaktadır:
1. **ROS 2 Düğümü (`moveit_to_abb.py`):** MoveIt'in `/display_planned_path` konusunu dinler, radyan cinsinden gelen eklem açılarını dereceye çevirir ve RWS servisleri aracılığıyla robota gönderir.
2. **RAPID Modülü (`ROS_Bridge`):** ABB tarafında çalışan, gelen `move_flag` sinyalini bekleyen ve `MoveAbsJ` komutu ile robotu hedef konuma süren sonsuz döngü programı.

---

## 📂 Proje İçeriği

* `moveit_to_abb.py` - ROS 2 MoveIt planlama köprü betiği.
* `ROS_Bridge_RAPID.txt` - ABB Kontrolcüsü için yazılmış RAPID kaynak kodu.

---

## 📦 Gereksinimler (Prerequisites)

Bu proje belirli bir işletim sistemi ve ROS 2 kombinasyonu üzerinde test edilmiş ve doğrulanmıştır. Sorunsuz bir kurulum için aşağıdaki ortamın sağlanması önerilir:

### 💻 Test Edilen Ortam
* **İşletim Sistemi:** Ubuntu 24.04.4 LTS (Noble Numbat)
* **ROS 2 Dağıtımı:** ROS 2 Jazzy Jalisco
* ** KULLANILAN DRİVER KAYNAKÇASI: ** [https://github.com/PickNikRobotics/abb_ros2/tree/jazzy](https://github.com/PickNikRobotics/abb_ros2/tree/jazzy)
* ** MOVEIT KAYNAKÇASI: ** https://moveit.picknik.ai/jazzy/index.html

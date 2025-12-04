Proje Özeti

Bu proje, 30 uçuşun 8 uçak (Veriler lisans probleminden dolayı küçültülmüştür) arasında zaman çakışması olmadan atanmasını amaçlayan uçuş atama problemini ele alır. Aynı veri seti üzerinde dört farklı yöntem uygulanmış ve performansları karşılaştırılmıştır: Gurobi, Simulated Annealing (SA), Tabu Search (TS) ve Genetic Algorithm (GA). Maliyet tüm yöntemlerde sabit olduğu için değerlendirme çözüm süresi, kararlılık ve arama davranışı üzerine odaklanmıştır.

Problem Tanımı

Her uçuşun tam olarak bir uçağa atanması, zamanları çakışan uçuşların aynı uçağa verilememesi ve en az bir uçuş alan her uçağın aktif kabul edilmesi gerekmektedir. Veri setindeki uçuş maliyetleri sabit olduğu için her algoritma aynı toplam maliyete ulaşmıştır.

Gurobi

Gurobi, karma tamsayılı programlama kullanarak problemi kesin olarak çözen bir optimizasyon aracıdır. Bu projede çözümü anında üretmiştir. Küçük ölçekli problemler için en hızlı ve en güvenilir yöntemdir. Ancak problem büyüdükçe çözüm maliyeti artabileceğinden geniş veri setlerinde meta-sezgisel yöntemlerin önemi artmaktadır.

Simulated Annealing (SA)

Simulated Annealing, yüksek sıcaklıklarda kötü çözümleri kabul ederek lokal minimumlardan kaçabilen probabilistik bir arama yöntemi kullanır. Sıcaklık azaldıkça daha seçici hâle gelir. Bu çalışmada optimal çözümü bulmuş ancak Gurobi ve Tabu Search’e kıyasla daha uzun sürede tamamlamıştır. Performansı parametre ayarlarına oldukça duyarlıdır.

Tabu Search (TS)

Tabu Search, komşu çözümleri keşfeden ve tabu listesi sayesinde yakın geçmişte denenmiş hareketlere geri dönmeyi engelleyen bir yöntemdir. Döngüye girmeden sistematik bir arama yapar. Uygulanan meta-sezgisel yöntemler arasında en hızlı ve en kararlı performansı göstermiştir ve optimal çözüme kısa sürede ulaşmıştır.

Genetic Algorithm (GA)

Genetic Algorithm, popülasyon tabanlı bir yönteme dayanır ve çözümleri seçme, çaprazlama ve mutasyon süreçleriyle geliştirir. Çözüm uzayında geniş bir arama yapabilir ancak diğer yöntemlere kıyasla daha uzun çalışma süresi gerektirmiştir. Birden fazla çalıştırmada performansı iyileşmiş olsa da en yavaş meta-sezgisel yöntem olmuştur.

Karşılaştırma ve Bulgular

Tüm yöntemler uçuşları zaman çakışması olmadan doğru şekilde atamış ve aynı maliyete ulaşmıştır. Aralarındaki fark, yalnızca hız ve kararlılık üzerinden ortaya çıkmıştır. Gurobi küçük ölçekler için en uygun araçtır. Tabu Search meta-sezgisel yöntemler içinde en hızlı ve en istikrarlı yöntemdir. Simulated Annealing daha yavaş ve parametreye duyarlıdır. Genetic Algorithm ise geniş arama kapasitesine sahip olmasına rağmen en uzun süreyi gerektirmiştir.

Genel Sonuç

Bu çalışma, kesin çözücüler ve meta-sezgisel algoritmaların aynı problem üzerinde nasıl davrandığını net bir şekilde göstermektedir. Gurobi hız ve doğruluk açısından öne çıkarken, Tabu Search meta-sezgiseller arasında en iyi performansı sergilemiştir. Simulated Annealing ve Genetic Algorithm ise belirli avantajlara sahip olsa da hız açısından daha geridedir. Büyük ölçekli problemlerde meta-sezgisel yöntemlerin değeri artmaktadır.

# GAME STUDIO — AI Game Development Team

Claude Code için yeniden kullanılabilir bir **yapay zekâ oyun stüdyosu**: tek bir merkezi
**koordinatör skill'i** (`SKILL.md`) ve gerçekten çağrılabilen **30 uzman subagent**.
Fikir aşamasından oynanabilir, test edilmiş ve paketlenmiş sürüme kadar bütün oyun
geliştirme sürecini yönetir. Godot, Unity, Unreal, Roblox, GameMaker, Defold, HTML5/Web ve
özel motorlarla çalışacak şekilde tasarlanmıştır.

Bu klasör bir Claude Code **plugin**'idir (`.claude-plugin/plugin.json`). Kurulduğunda:
- `game-studio` skill'i (koordinatör) → `/game-studio` ile ya da oyun geliştirme isteklerinde otomatik çağrılır,
- 30 uzman → `game-studio:<rol>` adlı subagent'lar olarak (`/agents` listesinde) görünür.

## Kurulum

### A) Global (önerilen — bütün projelerde kullanılır)
```bash
git clone https://github.com/rodinyamert48/gamer-studio-skill.git
```
```bash
cd gamer-studio-skill && ./scripts/install.sh
```
Betik, klasörü `~/.claude/skills/game-studio/` altına kopyalar (Claude Code bunu
`game-studio@skills-dir` plugin'i olarak otomatik yükler), ardından doğrulayıcıyı çalıştırır.
Var olan bir game-studio kurulumu önce `~/.claude/backups/` altına yedeklenir; aynı adlı
**başka** bir klasör varsa betik hiçbir şeyin üzerine yazmaz. Diğer skill ve agent'larınıza dokunmaz.

Seçenekler: `--link` (kopyalamak yerine sembolik bağ — skill'i geliştirirken), `--project <dir>`
(yalnızca bir projeye kur: `<dir>/.claude/skills/game-studio`), `--dry-run`.

### B) Plugin marketplace üzerinden
Claude Code içinde:
```
/plugin marketplace add rodinyamert48/gamer-studio-skill
/plugin install game-studio@game-studio-marketplace
```
Claude Code 2.1.275 ve sonrasında tek adımda:
```
/plugin install game-studio --marketplace rodinyamert48/gamer-studio-skill
```

### C) Tek oturumluk deneme
```bash
claude --plugin-dir /path/to/gamer-studio-skill
```

Kurulumdan sonra **yeni bir oturum açın** (veya `/reload-plugins`).

Kaldırma: `./scripts/uninstall.sh` (yedek bırakır).

## Kullanım

```
/game-studio Tarayıcıda oynanan, piksel sanatlı küçük bir platform oyunu yap
/game-studio Bu Godot projesine çift zıplama ve duvar kayması ekle
/game-studio qa
/game-studio status
/game-studio release — Windows EXE ve web sürümü hazırla
```
Skill'i adıyla çağırmak zorunda değilsiniz: "oyun yap", "bu oyuna ... ekle", "oyunu export et"
gibi istekler de skill'i tetikler.

Koordinatör sırasıyla şunu yapar:
1. **Sınıflandırma** — yeni proje / özellik / hata / küçük değişiklik / denge / QA / durum / yayın; ölçek (S/M/L/XL).
2. **Ortam taraması** — mevcut dosyalar, motor tespiti, kurulu araçlar (godot, node, dotnet, blender…).
3. **Ekip seçimi** — 30 uzmandan yalnızca gerekenleri seçer (küçük işte 1–3, büyük projede çok daha fazla).
4. **Görev kartları** — her uzmana bağımsız, dosya sahipliği belirtilmiş bir görev kartı gönderir.
5. **Paralel/sıralı yürütme** — bağımsız işler aynı anda (birden fazla agent çağrısı tek mesajda), bağımlı işler sırayla.
6. **Entegrasyon** — çıktıları birleştirir, çakışmaları çözer, etkilenen uzmanlara değişikliği iletir, derler.
7. **QA döngüsü** — QA hataları önem derecesiyle raporlar; koordinatör düzeltme görevleri açar; QA doğrular.
8. **Rapor** — Türkçe, kısa: ne yapıldı, nasıl çalıştırılır, test sonuçları (geçti / kaldı / çalıştırılmadı), riskler.

Proje içinde gerektiğinde `studio/` klasörü oluşturulur (`GDD.md`, `TECHNICAL_DESIGN.md`,
`TASKS.md`, `PROJECT_STATUS.md`, `DECISIONS.md`, `BUGS.md`, `QA_REPORT.md`…). Küçük işlerde
belge oluşturulmaz veya yalnızca kısa bir `BRIEF.md` yazılır.

## 30 uzman

| # | Agent (`game-studio:…`) | Görev |
|---|---|---|
| **A — Yönetim ve Tasarım** |||
| 01 | `executive-producer` | Hedefler, kapsam (MoSCoW/MVP), kaynak, kilometre taşı onayı (go/no-go) |
| 02 | `project-manager` | TASKS.md, bağımlılıklar, paralel iş grupları, durum raporu |
| 03 | `game-director` | Vizyon, tasarım sütunları, oynanış kalitesi denetimi |
| 04 | `creative-director` | Yaratıcı kimlik, ton, görsel/işitsel/anlatısal bütünlük |
| 05 | `technical-director` | Motor seçimi, mimari, TECHNICAL_DESIGN.md, kod standartları, kod incelemesi |
| 06 | `lead-game-designer` | GDD, ana oynanış döngüsü, mekanik spesifikasyonları |
| 07 | `systems-designer` | Statlar, denge, zorluk eğrisi, simülasyon betikleri |
| 08 | `level-designer` | Harita/bölüm tasarımı, akış, karşılaşmalar, greybox |
| 09 | `narrative-quest-designer` | Hikâye, karakter, diyalog, görev, oyun içi metinler |
| 10 | `economy-designer` | Para/kaynak, ödül, mağaza, ilerleme, grind analizi |
| **B — Kullanıcı Deneyimi ve Arayüz** |||
| 11 | `ux-designer` | Kontroller, akışlar, onboarding, kullanılabilirlik ve erişilebilirlik |
| 12 | `ui-visual-designer` | Menü/HUD tasarımı, UI stil rehberi, ikon, tipografi |
| 13 | `ui-engineer` | Arayüzlerin motorda kodlanması, çözünürlük uyumu, UI↔oyun bağlantısı |
| **C — Görsel Sanatlar ve Animasyon** |||
| 14 | `art-director` | Art bible, görsel stil, sanat denetimi |
| 15 | `concept-artist` | Konsept sayfaları, mood board, siluet çalışmaları |
| 16 | `character-artist` | Oyuncu/NPC/düşman görselleri |
| 17 | `environment-artist` | Tileset, arazi, arka plan, çevre giydirme |
| 18 | `props-artist` | Silah, eşya, araç, etkileşimli nesneler |
| 19 | `technical-artist` | Asset pipeline, shader/materyal, atlas, görsel performans, lisans takibi |
| 20 | `animator` | Animasyonlar, durum makineleri, geçişler, oyun hissi |
| 21 | `vfx-lighting-artist` | Efekt/parçacık, geri bildirim, ışık, atmosfer |
| **D — Yazılım ve Teknik Geliştirme** |||
| 22 | `gameplay-programmer` | Oyuncu kontrolü, temel mekanikler, oyun durumu, kayıt sistemi |
| 23 | `ai-programmer` | NPC/düşman davranışı, FSM/davranış ağacı, pathfinding |
| 24 | `physics-combat-programmer` | Çarpışma, fizik, hitbox, hasar, savaş hissi |
| 25 | `multiplayer-backend-engineer` | Netcode, sunucu, lobi, eşleştirme, çevrim içi veri, güvenlik |
| 26 | `tools-build-devops-engineer` | Build/export, EXE/web paketleri, CI, test altyapısı, geliştirici araçları |
| **E — Ses, Test ve Yayın** |||
| 27 | `sound-designer` | SFX, ortam sesleri, ses yöneticisi, miks |
| 28 | `composer` | Müzik, döngüler, dinamik müzik sistemi |
| 29 | `qa-engineer` | Test planı, otomatik testler, hata raporu, doğrulama, regresyon |
| 30 | `publishing-marketing-specialist` | Mağaza sayfası, sürüm notları, basın kiti, topluluk geri bildirimi |

Her uzman dosyası şunları içerir: sorumluluklar, girdiler, çıktılar, çalışma yöntemi, kalite
kontrol listesi, işbirliği ve bütün uzmanlarda ortak olan **Studio Protocol** (kapsam, dosya
sahipliği, gerçek kanıt kuralı, lisans, standart rapor formatı).

## Dosya yapısı

```
game-studio/
├── .claude-plugin/
│   ├── plugin.json          # plugin manifesti (skills: ["./"])
│   └── marketplace.json     # /plugin marketplace add için
├── SKILL.md                 # koordinatör — sistemin beyni
├── agents/                  # 30 uzman subagent (01-…md … 30-…md)
├── references/              # ihtiyaç olunca okunan ayrıntılı rehberler
│   ├── development-pipeline.md   # 7 aşama, kilometre taşları, kapı kriterleri
│   ├── project-management.md     # görev durumları, görev kartı, sürümleme, karar kaydı
│   ├── engine-guidelines.md      # motor tespiti/seçimi, build/run/test/export komutları
│   ├── coding-standards.md       # mimari, isimlendirme, motor idiomları, kod inceleme
│   ├── art-pipeline.md           # prosedürel/SVG/piksel sanat üretimi, isimlendirme, bütçeler, lisans
│   ├── audio-pipeline.md         # SFX/müzik üretimi, ses olayları, miks hedefleri
│   └── qa-standards.md           # önem dereceleri, hata raporu, test otomasyonu, Playwright
├── templates/               # GDD, TECHNICAL_DESIGN, TASKS, PROJECT_STATUS, BUGS, … şablonları
├── scripts/
│   ├── install.sh / uninstall.sh
│   └── validate.py          # yapısal doğrulayıcı (30 agent, frontmatter, tutarlılık)
├── README.md
└── LICENSE
```

Referanslar her çağrıda yüklenmez: koordinatör yalnızca ilgili dosyanın yolunu görev
kartına yazar, uzman onu kendisi okur. Bu, bağlam tüketimini düşük tutar.

## Paralel çalışma

Claude Code'un Agent aracı, aynı mesajda birden fazla subagent başlatarak **gerçek paralel**
çalışmayı destekler. Koordinatör bağımsız işleri (ör. farklı tasarımcıların belgeleri, ayrı
sanat kategorileri, ayrık dosya sahipliğine sahip kod modülleri) paralel başlatır; aynı
dosyayı iki uzmanın aynı anda yazmasına izin vermez (gerekirse `isolation: "worktree"`).
Subagent'lar başka subagent çağırmaz — iletişim koordinatör üzerinden (hub-and-spoke) ve
`studio/` belgeleriyle yapılır. Agent aracının bulunmadığı bir ortamda koordinatör, uzman
dosyalarını okuyup rolleri **sıralı** olarak kendisi uygular ve bunu kullanıcıya açıkça söyler.

## Doğrulama

```bash
python3 scripts/validate.py
```
```bash
claude plugin validate .
```

## Dil

Koordinatör kullanıcıyla kullanıcının dilinde (varsayılan Türkçe) konuşur; `studio/`
belgeleri görev kartındaki DOC LANGUAGE ile yazılır. Agent ve skill talimatları, her oturumda
yüklenen bağlamı küçük tutmak ve model tarafından en tutarlı şekilde izlenmesi için İngilizce yazılmıştır.

## Sınırlamalar

- Oyun motorlarının ikili dosyaları (Godot, Unity, Unreal…) bu plugin ile kurulmaz. Motor
  yoksa proje dosyaları yine üretilir; motor gerektiren derleme/testler **"bu ortamda doğrulanmadı"**
  olarak işaretlenir ve çalıştırılacak tam komut verilir. HTML5 oyunları ek kurulum olmadan
  (Playwright/Chromium ile) test edilebilir.
- Sanat ve ses, el çizimi yerine **kodla/prosedürel** (SVG, piksel betikleri, shader, Blender
  Python, sentez betikleri) veya lisansı doğrulanmış CC0/CC-BY kaynaklardan üretilir.
- Unreal `.uasset` gibi ikili formatlar doğrudan yazılamaz; C++/Python editör betikleri ve veri tabloları kullanılır.
- macOS/iOS derlemeleri macOS ve imzalama gerektirir.

## Lisans
MIT

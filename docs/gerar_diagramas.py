"""Gera os diagramas SVG do README. Uso: python3 docs/gerar_diagramas.py docs"""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
INK, MUTED, PAPER, CARD = "#1f2a24", "#5d6b62", "#f4f1e8", "#fbfaf5"
GREEN, BLUE, RED, AMBER, STEEL = "#2e7d4f", "#2b7a9b", "#c8402f", "#d99a1b", "#9aa59e"
MONO = 'ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace'
SANS = 'system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif'


def svg(w, h, body):
    markers = "".join(
        f'<marker id="a-{n}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c}"/></marker>'
        for n, c in (("ink", INK), ("green", GREEN), ("blue", BLUE), ("red", RED)))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">
<defs>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.1" fill="{INK}" opacity=".10"/></pattern>
{markers}
<style>
text{{font-family:{MONO};fill:{INK};font-size:12px}}
.h{{font-family:{SANS};font-weight:700;font-size:24px}}
.sub{{fill:{MUTED};font-size:13px}}
.b{{font-weight:700}}
.tag{{font-weight:700;font-size:11px;letter-spacing:1.5px}}
.m{{fill:{MUTED}}}
.w{{fill:#fff}}
.s{{font-size:11px}}
.c{{text-anchor:middle}}
.e{{text-anchor:end}}
.wire{{fill:none;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}}
</style>
</defs>
<rect width="{w}" height="{h}" rx="18" fill="{PAPER}"/>
<rect width="{w}" height="{h}" rx="18" fill="url(#dots)"/>
{body}
</svg>
'''


def t(x, y, s, cls="", extra=""):
    c = f' class="{cls}"' if cls else ""
    return f'<text x="{x}" y="{y}"{c}{extra}>{s}</text>'


# ───────────────────────── 1. arquitetura ─────────────────────────
def arquitetura():
    b = [t(40, 52, "Arquitetura", "h"),
         t(40, 76, "o ciclo da bomba roda dentro do ESP32; a nuvem serve só para ver e comandar de longe", "sub")]
    # casa
    b.append(f'<rect x="30" y="100" width="490" height="400" rx="14" fill="{CARD}" stroke="{INK}" stroke-width="1.2" stroke-dasharray="6 6"/>')
    b.append(t(50, 126, "SUA CASA · REDE LOCAL", "tag"))
    # torre
    b.append(t(130, 158, "torre · 30 cavidades", "c s"))
    b.append(f'<rect x="62" y="390" width="136" height="70" rx="8" fill="#cfe4ec" stroke="{INK}" stroke-width="1.5"/>')
    b.append(f'<rect x="112" y="170" width="36" height="222" rx="10" fill="#e3ebdf" stroke="{INK}" stroke-width="1.5"/>')
    for cx, cy in ((104, 200), (156, 240), (104, 280), (156, 320), (104, 360)):
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="13" ry="10" fill="{GREEN}"/>')
    b.append(f'<rect x="118" y="424" width="24" height="24" rx="4" fill="{INK}"/>')
    b.append(t(76, 412, "10 L", "s b"))
    b.append(t(130, 480, "bomba submersa 12 V", "c s"))
    # esp32
    b.append(f'<rect x="280" y="160" width="210" height="112" rx="10" fill="{INK}"/>')
    b.append(t(300, 196, "ESP32", "w b", ' style="font-size:20px"'))
    b.append(t(300, 217, "firmware ESPHome", "", ' fill="#b9d8c4"'))
    b.append(t(300, 242, "conta o tempo e aciona", "w s"))
    b.append(t(300, 258, "a bomba sozinho", "w s"))
    # rele
    b.append(f'<rect x="280" y="330" width="210" height="64" rx="10" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')
    b.append(t(300, 357, "Relé", "b", ' style="font-size:15px"'))
    b.append(t(300, 378, "liga/desliga a bomba", "s"))
    b.append(f'<line x1="385" y1="272" x2="385" y2="328" stroke="{INK}" stroke-width="2" marker-end="url(#a-ink)"/>')
    b.append(t(395, 306, "GPIO26", "s"))
    b.append(f'<path d="M280 362H222V436H146" class="wire" stroke="{RED}" stroke-width="2.5" marker-end="url(#a-red)"/>')
    b.append(f'<line x1="150" y1="212" x2="278" y2="212" stroke="{INK}" stroke-width="2" marker-end="url(#a-ink)"/>')
    b.append(t(214, 203, "sensores", "c s"))
    b.append(t(285, 430, "dashboard local, sem internet:", "s m"))
    b.append(t(285, 447, "http://torre-hidroponica.local", "s b"))
    # mqtt
    b.append(t(610, 172, "MQTT + TLS", "c b", f' fill="{GREEN}" style="font-size:13px"'))
    b.append(t(610, 190, "porta 8883", "c s", f' fill="{GREEN}"'))
    b.append(t(610, 228, "conexão de SAÍDA:", "c s m"))
    b.append(t(610, 244, "nenhuma porta aberta", "c s m"))
    b.append(t(610, 260, "no roteador", "c s m"))
    # vps
    b.append(f'<rect x="700" y="100" width="470" height="400" rx="14" fill="{CARD}" stroke="{INK}" stroke-width="1.2" stroke-dasharray="6 6"/>')
    b.append(t(720, 126, "VPS · DOCKER COMPOSE", "tag"))
    b.append(f'<line x1="490" y1="205" x2="728" y2="205" stroke="{GREEN}" stroke-width="2.5" marker-end="url(#a-green)"/>')
    b.append(f'<rect x="730" y="160" width="180" height="90" rx="10" fill="{GREEN}"/>')
    b.append(t(748, 196, "Mosquitto", "w b", ' style="font-size:17px"'))
    b.append(t(748, 217, "broker MQTT", "w"))
    b.append(t(748, 236, "usuário + senha + ACL", "w s"))
    b.append(f'<rect x="960" y="160" width="180" height="90" rx="10" fill="{BLUE}"/>')
    b.append(t(976, 196, "Home Assistant", "w b", ' style="font-size:16px"'))
    b.append(t(976, 217, "histórico, gráficos", "w s"))
    b.append(t(976, 234, "e automações", "w s"))
    b.append(f'<line x1="958" y1="205" x2="912" y2="205" stroke="{INK}" stroke-width="2" marker-end="url(#a-ink)" marker-start="url(#a-ink)"/>')
    b.append(t(935, 195, "1883", "c s"))
    b.append(t(935, 226, "interno", "c s m"))
    b.append(f'<rect x="960" y="350" width="180" height="80" rx="10" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')
    b.append(t(976, 382, "nginx", "b", ' style="font-size:16px"'))
    b.append(t(976, 404, "HTTPS · Let's Encrypt", "s"))
    b.append(f'<line x1="1050" y1="350" x2="1050" y2="252" stroke="{INK}" stroke-width="2" marker-end="url(#a-ink)"/>')
    b.append(t(1060, 306, "127.0.0.1:8123", "s"))
    b.append(t(720, 478, "exposto à internet: só 8883 (MQTT) e 443 (HTTPS)", "s m"))
    # voce
    b.append(f'<rect x="545" y="350" width="130" height="80" rx="12" fill="{INK}"/>')
    b.append(t(562, 380, "Você", "w b", ' style="font-size:16px"'))
    b.append(t(562, 400, "celular ou", "w s"))
    b.append(t(562, 416, "notebook", "w s"))
    b.append(f'<line x1="675" y1="390" x2="958" y2="390" stroke="{BLUE}" stroke-width="2.5" marker-end="url(#a-blue)"/>')
    b.append(t(820, 380, "HTTPS :443 · de qualquer lugar", "c s b", f' fill="{BLUE}"'))
    return svg(1200, 530, "\n".join(b))


# ───────────────────────── 2. ligações ─────────────────────────
def bloco(x, y, letras=("S", "V", "G")):
    out = []
    for i, l in enumerate(letras):
        cy = y - 16 + 16 * i
        out.append(f'<rect x="{x}" y="{cy - 8}" width="16" height="16" rx="2" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
        out.append(f'<text x="{x + 8}" y="{cy + 3.5}" class="c" style="font-size:9.5px;font-weight:700">{l}</text>')
    return "".join(out)


def modulo(x, y0, y1, titulo, linhas, planejado, w=240):
    dash = ' stroke-dasharray="6 5"' if planejado else ""
    fill = CARD if planejado else "#fff"
    out = [f'<rect x="{x}" y="{y0}" width="{w}" height="{y1 - y0}" rx="9" fill="{fill}" stroke="{INK}" stroke-width="1.5"{dash}/>']
    return out


def ligacoes():
    b = [t(40, 52, "Ligações no shield expansor", "h"),
         t(40, 76, "cada GPIO do shield tem 3 pinos: S (sinal) · V (alimentação) · G (terra)", "sub")]
    # shield + esp32
    b.append(f'<rect x="420" y="110" width="360" height="560" rx="16" fill="#dfe9dd" stroke="{INK}" stroke-width="1.5"/>')
    b.append(t(600, 656, "SHIELD EXPANSOR 30 PINOS", "c tag"))
    b.append(f'<rect x="575" y="140" width="50" height="26" rx="3" fill="{STEEL}" stroke="{INK}" stroke-width="1.2"/>')
    b.append(f'<rect x="525" y="158" width="150" height="470" rx="8" fill="{INK}"/>')
    b.append(f'<rect x="555" y="186" width="90" height="74" rx="4" fill="#c9d1cb"/>')
    b.append(t(600, 228, "WROOM-32", "c s b"))
    b.append(t(600, 420, "ESP32", "c w b", ' style="font-size:20px"'))
    b.append(t(600, 442, "DevKit", "c w s"))
    b.append(t(600, 102, "USB 5 V ← carregador de parede", "c b"))
    b.append(f'<line x1="600" y1="108" x2="600" y2="138" stroke="{INK}" stroke-width="2" marker-end="url(#a-ink)"/>')

    esq = {"D27": 200, "D26": 300, "D25": 390, "D33": 480, "D32": 570}
    for nome, y in esq.items():
        b.append(bloco(436, y))
        b.append(f'<line x1="452" y1="{y}" x2="525" y2="{y}" stroke="{MUTED}" stroke-width="1"/>')
        b.append(t(488, y - 6, nome, "c b"))
    # pino 5V dedicado
    b.append(f'<rect x="436" y="247" width="16" height="16" rx="2" fill="{RED}" stroke="{INK}" stroke-width="1.2"/>')
    b.append(t(460, 259, "5V", "b", f' fill="{RED}"'))
    # direita
    b.append(bloco(748, 390))
    b.append(f'<line x1="675" y1="390" x2="748" y2="390" stroke="{MUTED}" stroke-width="1"/>')
    b.append(t(712, 384, "D4", "c b"))
    b.append(f'<circle cx="660" cy="300" r="6" fill="#5fb3d9"/>')
    b.append(f'<line x1="675" y1="300" x2="792" y2="300" stroke="{MUTED}" stroke-width="1" stroke-dasharray="3 3"/>')
    b.append(t(800, 296, "D2 · LED azul onboard", "s b"))
    b.append(t(800, 312, "pisca a cada 1 s (sinal de vida)", "s m"))

    def wire(x1, y, x2, cor):
        return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" class="wire" stroke="{cor}"/><circle cx="{x1 if x1 < 430 else x2}" cy="{y}" r="4" fill="{cor}"/>'

    def caixa(x, y0, y1, planejado):
        dash = ' stroke-dasharray="6 5"' if planejado else ""
        return f'<rect x="{x}" y="{y0}" width="240" height="{y1 - y0}" rx="9" fill="{CARD if planejado else "#fff"}" stroke="{INK}" stroke-width="1.5"{dash}/>'

    # boia 1 (D27)
    b.append(caixa(60, 170, 230, True))
    b.append(t(76, 195, "Boia de nível 1", "b", ' style="font-size:13px"'))
    b.append(t(76, 214, "fecha contato com o GND", "s m"))
    b += [wire(300, 184, 436, AMBER), wire(300, 216, 436, INK)]
    # relé (D26)
    b.append(caixa(60, 240, 340, False))
    b.append(t(76, 268, "Módulo relé 5 V", "b", ' style="font-size:13px"'))
    b.append(t(76, 287, "2 canais · low-level", "s m"))
    b.append(t(76, 303, "optoacoplado", "s m"))
    b.append(t(76, 326, "contatos → bomba ↓", "s b", f' fill="{RED}"'))
    for y, lab, cor in ((255, "VCC", RED), (284, "IN1", AMBER), (316, "GND", INK)):
        b.append(t(290, y + 4, lab, "e s b"))
        b.append(wire(300, y, 436, cor))
    # boia 2 (D25)
    b.append(caixa(60, 360, 420, True))
    b.append(t(76, 385, "Boia de nível 2", "b", ' style="font-size:13px"'))
    b.append(t(76, 404, "pull-up interno do ESP32", "s m"))
    b += [wire(300, 374, 436, AMBER), wire(300, 406, 436, INK)]
    # pH (D33)
    b.append(caixa(60, 450, 510, True))
    b.append(t(76, 475, "Sensor pH PH-4502C", "b", ' style="font-size:13px"'))
    b.append(t(76, 494, "alimentado em 3,3 V", "s m"))
    for y, lab, cor in ((464, "Po", AMBER), (480, "V+", RED), (496, "G", INK)):
        b.append(t(290, y + 4, lab, "e s b"))
        b.append(wire(300, y, 436, cor))
    # TDS (D32)
    b.append(caixa(60, 540, 600, True))
    b.append(t(76, 565, "Sensor TDS (Gravity)", "b", ' style="font-size:13px"'))
    b.append(t(76, 584, "sempre em 3,3 V", "s m"))
    for y, lab, cor in ((554, "A", AMBER), (570, "+", RED), (586, "−", INK)):
        b.append(t(290, y + 4, lab, "e s b"))
        b.append(wire(300, y, 436, cor))
    # DS18B20 (D4)
    b.append(f'<rect x="900" y="356" width="240" height="68" rx="9" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')
    b.append(t(950, 384, "DS18B20 + adaptador", "b", ' style="font-size:13px"'))
    b.append(t(950, 403, "pull-up já embutido", "s m"))
    for y, lab, cor in ((374, "DAT", AMBER), (390, "VCC", RED), (406, "GND", INK)):
        b.append(t(908, y + 4, lab, "s b"))
        b.append(f'<line x1="764" y1="{y}" x2="900" y2="{y}" class="wire" stroke="{cor}"/><circle cx="900" cy="{y}" r="4" fill="{cor}"/>')
    b.append(f'<path d="M1140 390H1168V468" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    b.append(f'<rect x="1160" y="468" width="16" height="46" rx="6" fill="{STEEL}" stroke="{INK}" stroke-width="1.2"/>')
    b.append(t(1152, 496, "sonda dentro", "e s m"))
    b.append(t(1152, 511, "do reservatório", "e s m"))
    # notas
    b.append(f'<rect x="800" y="150" width="360" height="92" rx="8" fill="#fff" stroke="{INK}" stroke-width="1"/><rect x="800" y="150" width="6" height="92" fill="{AMBER}"/>')
    b.append(t(820, 174, "JUMPER DE TENSÃO DO SHIELD", "tag"))
    b.append(t(820, 196, "em 3,3 V → todo pino V entrega 3,3 V,", "s"))
    b.append(t(820, 212, "seguro para os sensores. O relé precisa", "s"))
    b.append(t(820, 228, "de 5 V: use o pino 5V dedicado.", "s"))
    b.append(f'<rect x="800" y="556" width="360" height="108" rx="8" fill="#fff" stroke="{INK}" stroke-width="1"/><rect x="800" y="556" width="6" height="108" fill="{GREEN}"/>')
    b.append(t(820, 580, "REGRAS DE PINOS DO ESP32", "tag"))
    b.append(t(820, 602, "• analógicos só nos GPIO 32–39 (ADC1):", "s"))
    b.append(t(834, 618, "o ADC2 para de ler com o Wi-Fi ligado", "s"))
    b.append(t(820, 634, "• GPIO 34–39 são só entrada", "s"))
    b.append(t(820, 650, "• GPIO 6–11: nunca usar", "s"))
    # legenda
    x = 40
    for cor, lab in ((RED, "alimentação"), (INK, "GND"), (AMBER, "sinal")):
        b.append(f'<line x1="{x}" y1="716" x2="{x + 34}" y2="716" class="wire" stroke="{cor}"/>')
        b.append(t(x + 44, 720, lab, "s"))
        x += 44 + len(lab) * 7 + 28
    b.append(f'<rect x="{x}" y="706" width="34" height="20" rx="4" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')
    b.append(t(x + 44, 720, "instalado e testado", "s"))
    x += 44 + 19 * 7 + 28
    b.append(f'<rect x="{x}" y="706" width="34" height="20" rx="4" fill="{CARD}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="6 5"/>')
    b.append(t(x + 44, 720, "planejado (ainda não ligado)", "s"))
    return svg(1200, 750, "\n".join(b))


# ───────────────────────── 3. relé + bomba ─────────────────────────
def rele():
    b = [t(40, 52, "Bomba no relé", "h"),
         t(40, 76, "só o fio positivo passa pelo relé; baixa tensão (12 V em corrente contínua) do começo ao fim", "sub")]
    # fonte
    b.append(f'<rect x="40" y="170" width="190" height="130" rx="10" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')
    b.append(t(58, 200, "Fonte 12 V · 1 A", "b", ' style="font-size:14px"'))
    b.append(t(58, 220, "bivolt 100–240 V", "s m"))
    b.append(t(58, 236, "na tomada", "s m"))
    b.append(t(220, 259, "+", "e b", f' fill="{RED}" style="font-size:16px"'))
    b.append(t(220, 289, "−", "e b", ' style="font-size:16px"'))
    # relé
    b.append(f'<rect x="440" y="110" width="320" height="170" rx="10" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')
    b.append(t(458, 138, "Módulo relé · canal 1", "b", ' style="font-size:14px"'))
    b.append(t(458, 158, "bobina comandada pelo GPIO26", "s m"))
    b.append(t(458, 174, "nível baixo = relé fechado", "s m"))
    for x, lab, sub in ((520, "NC", "sem uso"), (600, "COM", "meio"), (680, "NO", "aberto")):
        b.append(f'<rect x="{x - 14}" y="252" width="28" height="28" rx="4" fill="{STEEL}" stroke="{INK}" stroke-width="1.2"/>')
        b.append(f'<circle cx="{x}" cy="266" r="6" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
        b.append(t(x, 244, lab, "c b"))
    # símbolo da chave
    b.append(f'<line x1="600" y1="228" x2="600" y2="206" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<line x1="680" y1="228" x2="680" y2="206" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<line x1="600" y1="206" x2="668" y2="192" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>')
    b.append(f'<circle cx="600" cy="206" r="3.5" fill="{INK}"/><circle cx="680" cy="206" r="3.5" fill="{INK}"/>')
    b.append(t(700, 198, "contato", "s m"))
    # bomba
    b.append(f'<rect x="970" y="170" width="190" height="130" rx="10" fill="#cfe4ec" stroke="{INK}" stroke-width="1.5"/>')
    b.append(t(1012, 200, "Bomba submersa", "b", ' style="font-size:14px"'))
    b.append(t(1012, 220, "DC 5–12 V · 1–3 W", "s m"))
    b.append(t(1012, 236, "no reservatório", "s m"))
    b.append(t(982, 259, "+", "b", f' fill="{RED}" style="font-size:16px"'))
    b.append(t(982, 289, "−", "b", ' style="font-size:16px"'))
    # fios
    b.append(f'<path d="M230 254H330V350H600V282" class="wire" stroke="{RED}"/>')
    b.append(f'<path d="M680 282V350H900V254H970" class="wire" stroke="{RED}"/>')
    b.append(f'<path d="M230 284H290V410H935V284H970" class="wire" stroke="{INK}"/>')
    b.append(t(465, 340, "vermelho (+) da fonte → COM", "c s b", f' fill="{RED}"'))
    b.append(t(790, 340, "NO → vermelho (+) da bomba", "c s b", f' fill="{RED}"'))
    b.append(t(612, 400, "preto (−) segue direto, sem passar pelo relé", "c s b"))
    # corte
    b.append(f'<line x1="608" y1="350" x2="672" y2="350" stroke="{RED}" stroke-width="2" stroke-dasharray="3 6" opacity=".6"/>')
    b.append(t(640, 374, "fio cortado aqui", "c s m"))
    # notas
    b.append(f'<rect x="40" y="440" width="545" height="78" rx="8" fill="#fff" stroke="{INK}" stroke-width="1"/><rect x="40" y="440" width="6" height="78" fill="{GREEN}"/>')
    b.append(t(60, 464, "POR QUE NO (NORMALMENTE ABERTO)", "tag"))
    b.append(t(60, 486, "Se o ESP32 desligar, travar ou reiniciar, o contato abre", "s"))
    b.append(t(60, 502, "e a bomba para. O padrão seguro é bomba desligada.", "s"))
    b.append(f'<rect x="615" y="440" width="545" height="78" rx="8" fill="#fff" stroke="{INK}" stroke-width="1"/><rect x="615" y="440" width="6" height="78" fill="{AMBER}"/>')
    b.append(t(635, 464, "PLACA SEM SERIGRAFIA?", "tag"))
    b.append(t(635, 486, "Multímetro em continuidade, relé desligado: os dois bornes", "s"))
    b.append(t(635, 502, "que apitam são COM e NC. O que sobra é o NO.", "s"))
    return svg(1200, 548, "\n".join(b))


# ───────────────────────── 4. ciclo ─────────────────────────
def ciclo():
    b = [t(40, 52, "Ciclo automático da bomba", "h"),
         t(40, 76, "fase de transplante: 15 min ligada / 15 min desligada (depois de enraizar: 15 / 30)", "sub")]
    x0, wseg, y, h = 60, 180, 130, 46
    for i in range(6):
        on = i % 2 == 1
        x = x0 + i * wseg
        b.append(f'<rect x="{x}" y="{y}" width="{wseg - 4}" height="{h}" rx="8" fill="{BLUE if on else "#dcd8cb"}"/>')
        b.append(t(x + (wseg - 4) / 2, y + 29, "LIGADA" if on else "desligada", "c b" + (" w" if on else " m")))
        b.append(f'<line x1="{x}" y1="{y + h + 6}" x2="{x}" y2="{y + h + 14}" stroke="{INK}" stroke-width="1.2"/>')
        b.append(t(x, y + h + 30, "boot" if i == 0 else f"{i * 15} min", "c s"))
    b.append(t(x0 + 6 * wseg, y + h + 30, "…", "c s"))
    b.append(t(60, 252, "• Todo boot começa com a bomba desligada (restore_mode: ALWAYS_OFF).", "s"))
    b.append(t(60, 272, "• Ligar ou desligar a bomba à mão reinicia o cronômetro da fase.", "s"))
    b.append(t(60, 292, "• Chave “Ciclo Automático” desligada = cronômetro congelado, controle 100% manual.", "s"))
    return svg(1200, 322, "\n".join(b))


OUT.mkdir(parents=True, exist_ok=True)
for nome, fn in (("arquitetura", arquitetura), ("ligacoes", ligacoes), ("rele-bomba", rele), ("ciclo", ciclo)):
    (OUT / f"{nome}.svg").write_text(fn(), encoding="utf-8")
    print("ok", nome)

# Torre Hidropônica — Diário de Bordo

Automação de torre hidropônica (30 cavidades, reservatório 10L) com ESP32 + ESPHome + Home Assistant.

## Estado atual (25/07/2026)

| Sistema | Status |
|---|---|
| ESP32 na rede (OTA) | ✅ `torre-hidroponica.local` |
| DS18B20 (temperatura da água) | ✅ GPIO4, lendo a cada 5s |
| Relé canal 1 → BOMBA | ✅ **MARCO 09/08/2026: primeira irrigação via Wi-Fi!** Fio vermelho do cabo da fonte 12V cortado e ligado nos bornes COM (P2, meio) e NO (P1) — identificados por continuidade no multímetro (placa sem serigrafia). Ciclo automático gravado: 45min → 15min ON / 30min OFF, com chave "Ciclo Automatico" no dashboard para pausar. ESP32 alimentado por carregador USB de parede, independente do Mac |
| TDS (qualidade da água) | ❌ placa defeituosa — devolvida ao ML (08/2026), aguardando substituta. Diagnóstico: alimentação ok (3,3V em +/−), saída A morta (0V com sonda na água). ATENÇÃO: cabo do kit tinha cores FORA do padrão (vermelho ≠ VCC!) — sempre conferir serigrafia A/+/− antes de ligar. Config comentada no torre.yaml |
| pH | ⏳ aguardando kit de resistores (divisor de tensão) |
| Boias de nível | ⏳ aguardando entrega |
| Bomba d'água | ⏳ voltagem desconhecida — LER A ETIQUETA |

## Mapa lógico de GPIOs (vale para sempre, sobrevive à migração)

| GPIO | Função | Detalhe |
|---|---|---|
| GPIO2 | LED onboard | pisca 1s (heartbeat) |
| GPIO4 | DS18B20 (1-Wire) | módulo adaptador com pull-up embutido |
| GPIO26 | Relé IN1 | low-level trigger → `inverted: true` |
| GPIO32 | TDS (ADC1) | alimentar TDS SEMPRE em 3,3V |
| GPIO33 | pH (ADC1) — reservado | PLANO ATUALIZADO (09/08): PH-4502C alimentado em 3,3V (pino V da coluna D33) → saída nunca excede 3,3V → SEM divisor de tensão, SEM protoboard. Ligação direta: V+→V, G→G, Po→S da coluna D33 (3 jumpers F-F). Calibrar com sachês 4.01/6.86 (trimpot + software). Custo do atalho: menor resolução, ok para hobby |
| GPIO25 / GPIO27 | boias de nível — reservados | entrada com pull-up interno, boia fecha para GND |

Regras de pinos: ADC só nos GPIO 32–39 (ADC2 morre com WiFi). GPIO 34–39 são só-entrada. GPIO 6–11: nunca usar.

## Montagem física atual (protoboard — fase provisória)

ESP32 assentado DESLOCADO: fileira `3V3 GND D15 D2 D4...` na coluna `a`
(fileiras 24 no topo/USB até 10), fileira `VIN GND D13... D26... D32...`
PENDURADA no ar fora da borda esquerda (fêmea encaixa direto nos pinos).

Régua dos pinos pendurados (topo→base): 24=VIN, 23=GND, 22=D13, 21=D12,
20=D14, 19=D27, 18=D26, 17=D25, 16=D33, 15=D32, 14=D35, 13=D34, 12=VN, 11=VP, 10=EN.

| Conexão | Caminho |
|---|---|
| 3,3V → trilha vermelha | furo 24b |
| GND → trilha azul | furo 23b |
| DS18B20 DAT | módulo → furo 20b (nó do D4) |
| DS18B20 VCC/GND | trilhas vermelha/azul |
| Relé VCC | fêmea no pino pendurado VIN → 5a ═ 5b → VCC do módulo |
| Relé IN1 | fêmea no pino pendurado D26 → 3a ═ 3b → IN1 |
| Relé GND | trilha azul |
| TDS vermelho | soquete do bloco → trilha vermelha (3,3V! nunca VIN) |
| TDS preto | soquete do bloco → trilha azul |
| TDS amarelo | soquete do bloco → 7a ═ 7b → fêmea no pino pendurado D32 |

## Firmware

- Config: `esphome/torre.yaml` (+ `esphome/secrets.yaml` com WiFi, chave da API e senhas — fora do git; modelo em `esphome/secrets.example.yaml`)
- Gravar mudanças: `cd esphome && esphome run torre.yaml --device torre-hidroponica.local --no-logs`
- Logs ao vivo: `esphome logs torre.yaml --device torre-hidroponica.local`
- ESPHome CLI 2026.7.2 via Homebrew

## Front-ends

- Dashboard do ESP32 (web_server v3): http://torre-hidroponica.local (pede usuário/senha do secrets.yaml)
- Home Assistant (Docker/colima, config em `~/homeassistant`): http://localhost:8123
  - Integração ESPHome adicionada MANUALMENTE (host = IP do ESP32 na rede local, porta 6053, chave `api_encryption_key`) —
    mDNS não atravessa a VM do colima
- Futuro: MQTT → VPS (Mosquitto + InfluxDB + Grafana) + Uptime Kuma vigiando de fora

## Migração futura: shield expansor 30 pinos (em trânsito)

O shield replica cada GPIO em coluna S·V·G (sinal/alimentação/terra) e aceita fonte externa 6,5–16V.

Checklist da migração (~20 min, firmware NÃO muda):
1. Comprar jumpers F-F antes (~R$ 10) — shield→módulos é macho→macho
2. USB fora; desmontar jumpers da protoboard
3. Extrair ESP32 (alavanca alternada nas pontas) e encaixar nos soquetes do shield
4. Jumper amarelo de tensão do shield em 3.3V (TDS/pH/DS18B20 seguros)
5. Bloco fêmea do TDS → direto na coluna S·V·G do D32 (conferir ordem dos fios!)
6. DS18B20: F-F do módulo para coluna do D4
7. Relé: IN1 → S do D26 (F-F); VCC → pino dedicado 5V do shield; GND → G
8. Protoboard permanece só para o divisor de tensão do pH
9. Testar tudo nos dashboards antes de dar por migrado

## Pendências / compras

- [ ] Kit 600 resistores (em trânsito) → destrava pH
- [ ] Shield expansor (em trânsito) → migração acima
- [ ] Jumpers F-F (comprar)
- [ ] Água destilada (farmácia) → calibração do pH
- [x] **Bomba identificada (08/08/2026)**: MD:202506 2415-3, DC 5–12V, 1–3W, submersa. Fonte: BX-12001000, bivolt 100–240V → saída 12.0V/1A (12W). Cenário baixa tensão: relé chaveia o fio DC (um condutor cortado → bornes COM + NO do canal 1). Testada funcionando na torre antes da automação.
- [ ] Sachês calibração pH: em mãos ✓ (validade 10/01/2027)

## Cultivo (quando a eletrônica estabilizar)

- Folhosas de ciclo rápido primeiro (alface, rúcula); pH alvo 5,5–6,5
- Solução nutritiva A+B; ciclo inicial da bomba 15 min on / 30 min off
- Reservatório 10L: completar água a cada 1–2 dias, renovar solução a cada 10–15 dias

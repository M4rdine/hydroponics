# Torre Hidropônica — Diário de Bordo

Automação de torre hidropônica (30 cavidades, reservatório 10L) com ESP32 + ESPHome + Home Assistant.
Guia de montagem e diagramas: [README.md](README.md). Aqui ficam o estado do dia e o histórico.

## Estado atual (13/10/2026)

| Sistema | Status |
|---|---|
| ESP32 na rede (OTA) | ✅ `torre-hidroponica.local`, no shield expansor, alimentado por carregador USB de parede |
| Relé canal 1 → BOMBA | ✅ GPIO26. Fio vermelho da fonte 12V cortado e ligado nos bornes COM (P2, meio) e NO (P1) |
| Ciclo automático | ✅ 15 min ON / 15 min OFF (fase de transplante; o plano pós-enraizamento é 15/30). Chave "Ciclo Automatico" no dashboard pausa |
| Segurança do firmware | ✅ API com chave, OTA e dashboard com senha, MQTT só por TLS |
| Home Assistant | ✅ na VPS, por HTTPS, falando com o ESP32 por MQTT (ver Front-ends) |
| DS18B20 (temperatura da água) | ⚠️ testado e funcionando no GPIO4, mas DESCONECTADO desde 08/08: os 3 jumpers F-F dele foram para o relé. Religar nas colunas S·V·G do D4 |
| TDS (qualidade da água) | ❌ placa defeituosa devolvida em 08/2026; substituta a confirmar. Config comentada no `torre.yaml` |
| pH | ⏳ não ligado. Plano: PH-4502C em 3,3V direto no D33 (ainda não testado) |
| Boias de nível | ⏳ não ligadas (GPIO25 e GPIO27 reservados) |

## Mapa lógico de GPIOs

| GPIO | Função | Detalhe |
|---|---|---|
| GPIO2 | LED onboard | pisca 1s (heartbeat) |
| GPIO4 | DS18B20 (1-Wire) | módulo adaptador com pull-up embutido |
| GPIO26 | Relé IN1 | low-level trigger → `inverted: true` |
| GPIO32 | TDS (ADC1) | alimentar TDS SEMPRE em 3,3V |
| GPIO33 | pH (ADC1) — reservado | PH-4502C alimentado em 3,3V (pino V da coluna D33) → saída nunca excede 3,3V → sem divisor de tensão, sem protoboard. Ligação direta: V+→V, G→G, Po→S (3 jumpers F-F). Calibrar com sachês 4.01/6.86 (trimpot + software). Custo do atalho: menor resolução, ok para hobby |
| GPIO25 / GPIO27 | boias de nível — reservados | entrada com pull-up interno, boia fecha para GND |

Regras de pinos: ADC só nos GPIO 32–39 (ADC2 morre com WiFi). GPIO 34–39 são só-entrada. GPIO 6–11: nunca usar.

## Montagem física atual (shield expansor 30 pinos)

O shield replica cada GPIO em coluna S·V·G (sinal/alimentação/terra). Jumper amarelo de tensão em 3,3V.
Diagramas em `docs/ligacoes.svg` e `docs/rele-bomba.svg`.

| Conexão | Caminho |
|---|---|
| Relé IN1 | F-F → S da coluna D26 |
| Relé VCC | F-F → pino dedicado 5V do shield |
| Relé GND | F-F → G da coluna D26 |
| Bomba | fio vermelho (+) da fonte 12V → COM; NO → vermelho (+) da bomba; preto direto |
| DS18B20 (a religar) | DAT → S, VCC → V, GND → G da coluna D4 |
| TDS (quando voltar) | bloco fêmea direto na coluna S·V·G do D32 — conferir serigrafia A/+/− antes |

## Firmware

- Config: `esphome/torre.yaml` (+ `esphome/secrets.yaml` com WiFi, chave da API, senhas e MQTT — fora do git; modelo em `esphome/secrets.example.yaml`)
- Gravar mudanças: `cd esphome && esphome run torre.yaml --device torre-hidroponica.local --no-logs`
- Logs ao vivo: `esphome logs torre.yaml --device torre-hidroponica.local`
- ESPHome CLI 2026.7.2 via Homebrew
- `reboot_timeout: 0s` na API e no MQTT: sem isso o ESP32 reinicia a cada 15 min quando nenhum
  cliente usa a API, e cada boot recomeça o ciclo da bomba
- Sensor "Tempo Ligado" (uptime) denuncia reinícios inesperados

## Front-ends

- Dashboard do ESP32 (web_server v3): http://torre-hidroponica.local (pede usuário/senha do secrets.yaml)
- Home Assistant na VPS, acessível de qualquer lugar por HTTPS:
  - ESP32 → MQTT com TLS (porta 8883) → Mosquitto na VPS ← Home Assistant (mesma rede do compose)
  - Arquivos de deploy em `vps/` (compose em `/opt/torre` na VPS; domínio e senhas ficam fora do git)
  - HA atrás do nginx do host; no HA 2026.10 o proxy reverso é configurado pelo
    websocket `http/config/configure` + `http/config/promote` (ver `vps/homeassistant/configuration.yaml`)
  - Certificado Let's Encrypt renovado pelo certbot; hook copia para o Mosquitto (`vps/certbot-deploy-hook.sh`)
- Futuro: InfluxDB + Grafana e Uptime Kuma vigiando de fora

## Pendências

- [ ] Religar o DS18B20 (3 jumpers F-F na coluna D4)
- [ ] TDS: conferir se a placa substituta chegou; descomentar os blocos no `torre.yaml`
- [ ] pH: ligar no D33, acrescentar o sensor no firmware e calibrar (sachês vencem em 10/01/2027; água destilada para enxaguar o eletrodo)
- [ ] Boias de nível: 2 furos com vedação no reservatório, ligar nos GPIO25/27
- [ ] Passar o ciclo para 15/30 quando as plantas estiverem enraizadas (`fase_desligada_s: "1800"`)
- [ ] Acomodar a eletrônica na caixa estanque, se ainda não estiver
- [ ] Futuro: uma fonte 12V só para shield + bomba (entrada DC 6,5–16V do shield, com splitter P4)

## Cultivo

- Folhosas de ciclo rápido primeiro (alface, rúcula); pH alvo 5,5–6,5
- Solução nutritiva A+B
- Reservatório 10L: completar água a cada 1–2 dias, renovar solução a cada 10–15 dias

## Linha do tempo

- **25/07/2026** — Montagens 1 a 3 na protoboard: ESP32 na rede, DS18B20 lendo no GPIO4, relé no GPIO26 testado, TDS no GPIO32 em andamento. Dashboard do ESP32 e Home Assistant em Docker (colima) no Mac.
- **08/2026** — Placa TDS diagnosticada como defeituosa (alimentação ok, saída A em 0V com a sonda na água) e devolvida. O cabo do kit tinha cores fora do padrão (vermelho ≠ VCC).
- **08/08/2026** — Bomba identificada pela etiqueta: MD:202506 2415-3, DC 5–12V, 1–3W, submersa. Fonte BX-12001000, bivolt 100–240V → 12,0V/1A. Migração da protoboard para o shield concluída; DS18B20 ficou sem jumpers.
- **09/08/2026** — **Primeira irrigação via Wi-Fi.** Bornes do relé identificados por continuidade no multímetro (placa sem serigrafia). Ciclo automático no ar, ESP32 independente do Mac.
- **20/09/2026** — Home Assistant do Mac desligado (pesava no computador). Sem cliente na API, o ESPHome reinicia a placa a cada 15 min (comportamento padrão, pela documentação); só percebi em outubro.
- **13/10/2026** — Repositório publicado no GitHub. Firmware protegido (chave na API, senhas no OTA e no dashboard). Home Assistant e Mosquitto migrados para a VPS, com MQTT por TLS. `reboot_timeout: 0s` e sensor de uptime. README com diagramas.

### Histórico: montagem na protoboard (até 08/08/2026)

ESP32 assentado DESLOCADO: fileira `3V3 GND D15 D2 D4...` na coluna `a` (fileiras 24 no topo/USB até 10),
fileira `VIN GND D13... D26... D32...` pendurada fora da borda esquerda (fêmea encaixa direto nos pinos).
Régua dos pinos pendurados (topo→base): 24=VIN, 23=GND, 22=D13, 21=D12, 20=D14, 19=D27, 18=D26, 17=D25,
16=D33, 15=D32, 14=D35, 13=D34, 12=VN, 11=VP, 10=EN.

| Conexão | Caminho |
|---|---|
| 3,3V → trilha vermelha | furo 24b |
| GND → trilha azul | furo 23b |
| DS18B20 DAT | módulo → furo 20b (nó do D4) |
| DS18B20 VCC/GND | trilhas vermelha/azul |
| Relé VCC | fêmea no pino pendurado VIN → 5a ═ 5b → VCC do módulo |
| Relé IN1 | fêmea no pino pendurado D26 → 3a ═ 3b → IN1 |
| Relé GND | trilha azul |
| TDS | vermelho → trilha 3,3V (nunca VIN), preto → trilha azul, amarelo → 7a ═ 7b → D32 |

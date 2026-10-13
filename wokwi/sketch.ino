// Torre Hidroponica — simulacao Wokwi
// Espelha a montagem real: DS18B20 no GPIO4, rele no GPIO26, TDS no GPIO32.
// No Wokwi o sensor TDS e representado por um potenciometro: girar o knob
// simula a agua ficando mais/menos concentrada em sais.

#include <OneWire.h>
#include <DallasTemperature.h>

const int PIN_LED = 2;
const int PIN_DS18B20 = 4;
const int PIN_RELE = 26;    // low-level trigger: LOW = rele fechado
const int PIN_TDS = 32;

const unsigned long CICLO_BOMBA_LIGADA_MS = 8000;   // na vida real: 15 min
const unsigned long CICLO_BOMBA_DESLIGADA_MS = 8000; // na vida real: 30 min

OneWire oneWire(PIN_DS18B20);
DallasTemperature ds18b20(&oneWire);

unsigned long ultimaLeitura = 0;
unsigned long ultimaTrocaBomba = 0;
bool bombaLigada = false;

float lerTdsPpm(float temperaturaC) {
  int leitura = analogRead(PIN_TDS);          // 0..4095
  float tensao = leitura * 3.3 / 4095.0;
  float coef = 1.0 + 0.02 * (temperaturaC - 25.0);
  float vc = tensao / coef;
  return (133.42 * vc * vc * vc - 255.86 * vc * vc + 857.39 * vc) * 0.5;
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_RELE, OUTPUT);
  digitalWrite(PIN_RELE, HIGH);  // HIGH = rele aberto (bomba desligada)
  ds18b20.begin();
  Serial.println("Torre Hidroponica — simulacao iniciada");
}

void loop() {
  // heartbeat
  digitalWrite(PIN_LED, (millis() / 1000) % 2);

  // leituras a cada 3s
  if (millis() - ultimaLeitura > 3000) {
    ultimaLeitura = millis();
    ds18b20.requestTemperatures();
    float temp = ds18b20.getTempCByIndex(0);
    float tds = lerTdsPpm(temp);
    Serial.printf("Temperatura: %.1f C | TDS: %.0f ppm | Bomba: %s\n",
                  temp, tds, bombaLigada ? "LIGADA" : "desligada");
  }

  // ciclo automatico da bomba (versao acelerada para simulacao)
  unsigned long alvo = bombaLigada ? CICLO_BOMBA_LIGADA_MS : CICLO_BOMBA_DESLIGADA_MS;
  if (millis() - ultimaTrocaBomba > alvo) {
    ultimaTrocaBomba = millis();
    bombaLigada = !bombaLigada;
    digitalWrite(PIN_RELE, bombaLigada ? LOW : HIGH);
    Serial.printf(">>> Bomba %s (ouca o clique do rele)\n",
                  bombaLigada ? "LIGADA" : "DESLIGADA");
  }
}

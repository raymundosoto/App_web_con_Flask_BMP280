#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

const char* ssid = "Totalplay-319F_2.4Gnormal"; // Reemplaza con el nombre de tu red WiFi
const char* password = "319FEF5D88K2kS97"; // Reemplaza con la contraseña de tu red WiFi

Adafruit_BMP280 bmp; // Inicializa el sensor BMP280

void setup() {
  Serial.begin(115200);
  delay(100);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }

  if (!bmp.begin(0x76)) {
    Serial.println(F("No se pudo encontrar el sensor BMP280. Conexión fallida."));
    while (1);
  }

  configTime(0, 0, "pool.ntp.org"); // Configura el servidor NTP
}

void loop() {
  float temperatura = bmp.readTemperature();
  float presion = bmp.readPressure() / 100.0F; // Convertir a hPa
  float altitud = bmp.readAltitude(1013.25);

  // Crear el objeto JSON con los datos
  StaticJsonDocument<200> jsonDocument;
  jsonDocument["id_sensor"] = "bmp280";
  jsonDocument["timestamp"] = obtenerTimestamp();
  jsonDocument["temperatura"] = temperatura;
  jsonDocument["presion"] = presion;
  jsonDocument["altitud"] = altitud;

  // Imprimir el JSON en el monitor serial
  serializeJsonPretty(jsonDocument, Serial);
  Serial.println();

  // Convertir el objeto JSON a una cadena
  String jsonString;
  serializeJson(jsonDocument, jsonString);

  // Enviar los datos al servidor Flask
  HTTPClient http;
  http.begin("http://raymundosoto.pythonanywhere.com/datos"); // Reemplaza con la dirección de tu servidor Flask
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonString);
  
  if (httpResponseCode > 0) {
    Serial.print("Respuesta del servidor: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("Error en la conexión: ");
    Serial.println(httpResponseCode);
  }

  http.end();

  delay(5000); // Espera 5 segundos antes de enviar los datos nuevamente
}

String obtenerTimestamp() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Error al obtener la hora local");
    return "No hay hora";
  }

  char days[3], months[3], years[5], hours[3], minutes[3], seconds[3];

  sprintf(days, "%02d", timeinfo.tm_mday);
  sprintf(months, "%02d", timeinfo.tm_mon + 1);
  sprintf(years, "%04d", timeinfo.tm_year + 1900);
  sprintf(hours, "%02d", timeinfo.tm_hour);
  sprintf(minutes, "%02d", timeinfo.tm_min);
  sprintf(seconds, "%02d", timeinfo.tm_sec);

  String timestamp = String(years) + "-" + String(months) + "-" + String(days) + " " + 
                     String(hours) + ":" + String(minutes) + ":" + String(seconds);

  return timestamp;
}

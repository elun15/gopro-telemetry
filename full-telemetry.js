const gpmfExtract = require('gpmf-extract');
const goproTelemetry = require(`gopro-telemetry`);
const fs = require('fs');
 
const file = fs.readFileSync('./src/video5/video5.MP4');
 
gpmfExtract(file)
.then(extracted => {
goproTelemetry(extracted, {}, telemetry => {
fs.writeFileSync('./src/video5/prueba-video5-full-telemetry.json', JSON.stringify(telemetry));
console.log('Telemetry saved as JSON');
});
})
.catch(error => console.error(error));

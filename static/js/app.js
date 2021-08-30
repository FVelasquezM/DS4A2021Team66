const $checkCultivos = document.getElementById('check-cultivos')
const $checkConstrucciones = document.getElementById('check-construcciones')
const $checkBosques = document.getElementById('check-bosques')
const $checkLotesPastoreo = document.getElementById('check-lotesPastoreo')
const $checkRecursosHidricos = document.getElementById('check-recursosHidricos')
const $checkCarreteras = document.getElementById('check-carreteras')
const $checkViviendas = document.getElementById('check-viviendas')
const $checkAleoductos = document.getElementById('check-aleoductos')
const $checkRios = document.getElementById('check-rios')
const $checkMontañas = document.getElementById('check-montañas')

const $myChart = document.getElementById('myChart').getContext("2d")

class Data_barplot {
    constructor(cultivos=false, construcciones=false, bosques=false, lotesPastoreo=false, recursosHidricos=false, carreteras=false, viviendas=false, aleoductos=false, rios=false, montañas=false) {
      this.cultivos = cultivos;
      this.construcciones = construcciones;
      this.bosques = bosques;
      this.lotesPastoreo = lotesPastoreo;
      this.recursosHidricos = recursosHidricos;
      this.carreteras = carreteras;
      this.viviendas = viviendas;
      this.aleoductos = aleoductos
      this.rios = rios;montañas
      this.montañas = montañas;
    }

    get_cultivos() {
        return this.cultivos
    }
    get_construcciones() {
        return this.construcciones
    }
    get_bosques() {
        return this.bosques
    }
    get_lotesPastoreo() {
        return this.lotesPastoreo
    }
    get_recursosHidricos() {
        return this.recursosHidricos
    }
    get_carreteras() {
        return this.carreteras
    }
    get_viviendas() {
        return this.viviendas
    }
    get_aleoductos() {
        return this.aleoductos
    }
    get_rios() {
        return this.rios
    }
    get_montañas() {
        return this.montañas
    }
    
    set_cultivos(cultivos) {
        this.cultivos = cultivos
    }
    set_construcciones(construcciones) {
        this.construcciones = construcciones
    }
    set_bosques(bosques) {
        this.bosques = bosques
    }
    set_lotesPastoreo(lotesPastoreo) {
        this.lotesPastoreo = lotesPastoreo
    }
    set_recursosHidricos(recursosHidricos) {
        this.recursosHidricos = recursosHidricos
    }
    set_carreteras(carreteras) {
        this.carreteras = carreteras
    }
    set_viviendas(viviendas) {
        this.viviendas = viviendas
    }
    set_aleoductos(aleoductos) {
        this.aleoductos = aleoductos
    }
    set_rios(rios) {
        this.rios = rios
    }
    set_montañas(montañas) {
        this.montañas = montañas
    }

    return_values(){
        let values = {
            "cultivos": this.get_cultivos(),
            "construcciones": this.get_construcciones(),
            "bosques": this.get_bosques(),
            "lotesPastoreo": this.get_lotesPastoreo(),
            "recursosHidricos": this.get_recursosHidricos(),
            "carreteras": this.get_carreteras(),
            "viviendas": this.get_viviendas(),
            "aleoductos": this.get_aleoductos(),
            "rios": this.get_rios(),
            "montañas": this.get_montañas()
        }
        return values
    }

    async set_data(){
        const urlGetData = "http://127.0.0.1:5000/data-barplot"
        const settings = {
            method: "GET"
        };
        const res = await fetch(`${urlGetData}`, settings);
        const data = await res.json()
        return data
    }

  }

const data_barplot = new Data_barplot()

const resetCanvas = () =>{
    myChart.destroy(); // this is my <canvas> element
    canvas = document.getElementById('myChart');
    ctx = canvas.getContext('2d');
  };

const settingsCharBarplot = async () => {

    const colors = {
        "cultivos":'rgb(203,0,0)',
        "construcciones":'rgb(255,0,0)',
        "bosques":'rgb(0,0,0)',
        "lotesPastoreo":'rgb(217,101,69)',
        "recursosHidricos":'rgb(71,143,0)',
        "carreteras":'rgb(255,255,166)',
        "viviendas":'rgb(0,206,242)',
        "aleoductos":'rgb(69,224,245)',
        "rios":'rgb(255,255,255)',
        "montañas":'rgb(0,0,0)'
    }

    const set_labels = async () =>{
        labels = []
        const data_labels = data_barplot.return_values()
        const data = await data_barplot.set_data()
        let data_array = [
            [[data_labels.cultivos,"cultivos"], data.cultivos],
            [[data_labels.construcciones,"construcciones"], data.construcciones],
            [[data_labels.bosques, "bosques"], data.bosques],
            [[data_labels.lotesPastoreo,"lotesPastoreo"], data.lotesPastoreo],
            [[data_labels.recursosHidricos,"recursosHidricos"], data.recursosHidricos],
            [[data_labels.carreteras,"carreteras"], data.carreteras],
            [[data_labels.viviendas,"viviendas"], data.viviendas],
            [[data_labels.aleoductos,"aleoductos"], data.aleoductos],
            [[data_labels.rios,"rios"], data.rios],
            [[data_labels.montañas,"montañas"], data.montañas]
        ]
        let data_exportLabels = []
        let data_exportDatas = []
        data_array.map((e)=>{
            if(e[0][0]){
                data_exportLabels.push(e[0][1])
                data_exportDatas.push(e[1])
            }
        })
        return [data_exportLabels, data_exportDatas]
    }

    const set_colors = (array) =>{
        let data_colors = []
        array.map((e)=>data_colors.push(colors[e]))
        return data_colors
    }

    const print_data = await set_labels()

    const settings = {
        type: print_data[0].length > 4 ? "doughnut":"bar",
        data :{
            labels:print_data[0],
            datasets: [{
                label: 'Quantity',
                data: print_data[1].map(e => parseInt(e, 10)),
                backgroundColor: set_colors(print_data[0])
            }]
        },
        options:{
            scales: {
                yAxes:[{
                    ticks:{
                        beginAtZero:true
                    }
                }]
            },
            aspectRatio: 2,
            responsive:false
        }
    }
    console.log(print_data[0])
    console.log(print_data[1].map(e => parseInt(e, 10)))
    return settings
}

myChart = new Chart($myChart, {
    type: "bar" ,
    data :{
        labels: [],
        datasets: [{
            label: 'Quantity',
            data: [],
            backgroundColor: []
        }]
    },
    options:{
        scales: {
            yAxes:[{
                ticks:{
                    beginAtZero:true
                }
            }]
        },
        aspectRatio: 2,
        responsive:false
    }
})

$checkCultivos.onclick = async (e) =>{
    myChart.destroy()
    data_barplot.set_cultivos(e.target.checked)
    myChart = new Chart($myChart, await settingsCharBarplot())
}
$checkConstrucciones.onclick = async (e) =>{
    myChart.destroy()
    data_barplot.set_construcciones(e.target.checked)
    myChart = new Chart($myChart, await settingsCharBarplot())
}
$checkBosques.onclick = async (e) =>{
    myChart.destroy()
    data_barplot.set_bosques(e.target.checked)
    myChart = new Chart($myChart, await settingsCharBarplot())
}
$checkLotesPastoreo.onclick = async (e) =>{
    myChart.destroy()
    data_barplot.set_lotesPastoreo(e.target.checked)
    myChart = new Chart($myChart, await settingsCharBarplot())
}
$checkRecursosHidricos.onclick = async (e) =>{
    myChart.destroy()
    data_barplot.set_recursosHidricos(e.target.checked)
    myChart = new Chart($myChart, await settingsCharBarplot())
}
$checkCarreteras.onclick = async (e) =>{
    myChart.destroy()
    data_barplot.set_carreteras(e.target.checked)
    myChart = new Chart($myChart, await settingsCharBarplot())
}
$checkViviendas.onclick = async (e) =>{
    myChart.destroy()
    data_barplot.set_viviendas(e.target.checked)
    myChart = new Chart($myChart, await settingsCharBarplot())
}
$checkAleoductos.onclick = async (e) =>{
    myChart.destroy()
    data_barplot.set_aleoductos(e.target.checked)
    myChart = new Chart($myChart, await settingsCharBarplot())
}
$checkRios.onclick = async (e) =>{
    myChart.destroy()
    data_barplot.set_rios(e.target.checked)
    myChart = new Chart($myChart, await settingsCharBarplot())
}
$checkMontañas.onclick = async (e) =>{
    myChart.destroy()
    data_barplot.set_montañas(e.target.checked)
    myChart = new Chart($myChart, await settingsCharBarplot())
}
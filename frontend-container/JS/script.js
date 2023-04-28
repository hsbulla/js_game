//Создание мира
let canvas = window.document.querySelector('#render-canvas');
//Создание движка
let engine = new BABYLON.Engine(canvas);
//Создание сцены и присоединение её к движку
let scene = new BABYLON.Scene(engine);
scene.clearColor = new BABYLON.Color3(0.3, 0.3, 0.3);
scene.enablePhysics();//Подключаем физику к игре
scene.createDefaultEnvironment({
    createSkybox: false,
    createGround: false,
    cameraContrast: 1.7,
    cameraExposure: 1.1
});
//Создание фона



//Создание камеры
let camera = new BABYLON.FreeCamera('camera', new BABYLON.Vector3(0, 5, -30), scene);
camera.setTarget(new BABYLON.Vector3(0, 0, 0));
//Создание света - точечный свет
let light = new BABYLON.PointLight('light', new BABYLON.Vector3(10, 10, 0), scene);
light.intensity = 0.2;
//Создание генератора теней
let shadowGenerator = new BABYLON.ShadowGenerator(1024, light);

//Создание платформы и материала для неё
const createPlatform = (zPos) => {
    let platform = new BABYLON.MeshBuilder.CreateBox('box', {
        width: 6,
        height: 0.1,
        depth: 6,
        wrap: true
    }, scene);
    let boxMaterial = new BABYLON.StandardMaterial('marerial', scene);
    boxMaterial.emissiveTexture = new BABYLON.Texture(pathToImage_platform); 
    platform.material = boxMaterial;
    platform.receiveShadows = true;
    platform.physicsImpostor = new BABYLON.PhysicsImpostor(
        platform,
        BABYLON.PhysicsImpostor.BoxImpostor, { //Физические свойства
        mass: 0
    },
        scene);
    platform.position.z = zPos;
}

// Создание монетки
let coinArray = [];
const createCoin = (pos) => {
    BABYLON.SceneLoader.ImportMesh(
        null,
        pathToImage_coin,
        'scene.gltf',
        scene,
        (meshArray) => {
            let coin = meshArray[0];
            coin.scaling = new BABYLON.Vector3(0.04, 0.04, 0.04,); //Размер монетки
            coin.position = pos //Позиция монетки
            shadowGenerator.addShadowCaster(coin); //создание тени
            coin.receiveShadows = true;
            coinArray.push(coin);
        }
    )
}


//Создание препядствий
let lastRand = 0;//Глобальная переменная
let boxArray = []; //Массив для хранения всех блоков
let pointArray = []
const CreateBox = (xPos, zPos) => {
    let box = new BABYLON.MeshBuilder.CreateBox('box', {
        width: 2,
        height: 1,
        depth: 1
    }, scene);
    box.position = new BABYLON.Vector3(xPos, 0.6, 3 + zPos) //Координаты
    let boxMaterial = new BABYLON.StandardMaterial('marerial', scene);
    boxMaterial.emissiveTexture = new BABYLON.Texture(pathToImage_obstacle); 
    box.material = boxMaterial;
    box.receiveShadows = true;
    box.physicsImpostor = new BABYLON.PhysicsImpostor(
        box,
        BABYLON.PhysicsImpostor.BoxImpostor,
        {
            mass: 0
        },
        scene);
    shadowGenerator.getShadowMap().renderList.push(box); //Для теней
    box.receiveShadows = true;
    boxArray.push(box);
}
const CreateBoxRow = (zPos) => { //Этим мы обозначаем ряд препядствий
    let rand = Math.floor(Math.random() * 3) //для коробки, которая не отображается
    while (rand === lastRand) {
        rand = Math.floor(Math.random() * 3)
    }
    lastRand = rand;
    for (let i = 0; i < 3; i++) {
        if (i === rand) {
            if (Math.random() < 0.65) {   //Создание монетки с шансом 65% между препядствиями
                createCoin(new BABYLON.Vector3((i * 2) - 2, 1, 3 + zPos))
            }

            pointArray.push(new BABYLON.Vector3((i * 2) - 2, 1, 3 + zPos))    //создание невидимых точек
            continue;

        };
        CreateBox((i * 2 - 2), zPos);
    }
}



//Создание героя и материала для него
let Garry = new BABYLON.MeshBuilder.CreateSphere('sphere', {
    diameter: 0.8
}, scene);
Garry.position.y = 0.6;
let GarryMaterial = new BABYLON.StandardMaterial('material', scene);
GarryMaterial.emissiveTexture = new BABYLON.Texture(pathToImage_garry);
Garry.material = GarryMaterial;
shadowGenerator.getShadowMap().renderList.push(Garry);
Garry.physicsImpostor = new BABYLON.PhysicsImpostor(
    Garry,
    BABYLON.PhysicsImpostor.SphereImpostor, { //Присваеваем объекту физические свойства
    mass: 1,
    friction: 5 //трение
},
    scene);

for (let i = 0; i < 6; i++) {
    createPlatform(i * 6);
    if (i === 0) continue;
    CreateBoxRow(i * 6);
}

//Алгоритм
//Извлеченеи тегов из разметки
let restartBtn = window.document.querySelector('restart-btn');
let scoreInfo = window.document.querySelector('#score'); // переменная которая выводит очки на экран
let coininfo = window.document.querySelector('#coin-score'); // переменная которая выводит количество монет на экран
let playScreen = window.document.querySelector('#play-screen');
let gameOverScreen = window.document.querySelector('#game-over-screen');
let bestScoreInfo = window.document.querySelector('#best-score');
let nowScoreInfo = window.document.querySelector('#now-score');
//Константы
const PLAY = 'play';
const GAME_OVER = 'game-over';
//Переменные
let score = 0; //переменная для подсчета очков
let coin = 0; //переменная для подсчета монет
let state = PLAY; //Текущее состояние приложения
//Функции
const newRoadBlock = (zPos) => {
    createPlatform(zPos*6);
    CreateBoxRow(zPos*6);

}
const saveCoin = () => {
    window.localStorage.setItem('coin', coin);
}
const loadCoin = () => {
        coin = (window.localStorage.getItem('coin'))
            ? window.localStorage.getItem('coin')
            : 0
            ;
        coininfo.innerText = coin;
    }
const saveBestScore = () => {
    window.localStorage.setItem('bestScore', score);
}
const loadBestScore = () => {
    return (window.localStorage.getItem('bestScore'))
        ? window.localStorage.getItem('bestScore')
        : 0
    ;
}
const setgameOverScreen = () => { //Окно GAME OVER
    state = GAME_OVER;
    playScreen.style.display = 'none'; 
    gameOverScreen.style.display = 'block';
    let bestScore = loadBestScore();
    if (score > bestScore){
        saveBestScore();
        bestScore = score;
    }
    bestScoreInfo.innerText = `BEST: ${bestScore}`;
    nowScoreInfo.innerText = `NOW: ${score}`;
}

loadCoin();
//Встроенные функции Babylon.js
scene.registerBeforeRender(() => { //Проверка не столкнулся ли мяч с препядствиями
    for (let i = 0; i < boxArray.length; i++) {
        if (Garry.intersectsMesh(boxArray[i], true)) {
            boxArray[i].material.emissiveColor = new BABYLON.Color3(0.5, 0, 0);
            setgameOverScreen();
        }
    }
    for (let i = 0; i < coinArray.length; i++) {  //Проверка не столкнулся ли мяч с монеткой
        if (Garry.intersectsMesh(coinArray[i], false)) {
            coin++;
            coininfo.innerText = coin;
            saveCoin();
            coinArray[i].dispose(); //удаление объекта со сцены 
            coinArray.splice(i, 1)// //При первом столкновении удаляется монетка
        }
    }
    for (let i = 0; i < pointArray.length; i++) {  //Проверка на столкновение с невидимой точкой
        if (Garry.intersectsPoint(pointArray[i])) {
            scoreInfo.innerText = score;
            score++;
            pointArray.splice(i, 1); //При первом столкновении невидимый куб удаляется
            if (pointArray.length <= 4){
                newRoadBlock((pointArray[pointArray.length - 1].z+3)/6);
            }
        }
    }
})
engine.runRenderLoop(() => {
    camera.position.z = Garry.getAbsolutePosition().z - 12;
    light.position.z = Garry.getAbsolutePosition().z;
    scene.render();
});

//Обработчики событий
restartBtn = document.querySelector('.restsrt-btn'); //перезагрузка
document.addEventListener('keydown', (event) => { //кнопочка enter
    if (event.keyCode === 13) {
        window.location.reload()
    }
});

window.addEventListener('keypress', (event) => {//Управление WASD
    if (state !== GAME_OVER){
    let x = event.keyCode;
    if (event.key == 'a' || event.key == 'A' || event.key == 'ф' || event.key == 'Ф') {
        Garry.physicsImpostor.applyImpulse(
            new BABYLON.Vector3(-15, 0, 0),
            Garry.getAbsolutePosition()
        );
    }
    let y = event.keyCode;
    if (event.key == 'd' || event.key == 'D' || event.key == 'в' || event.key == 'В') {
        Garry.physicsImpostor.applyImpulse(
            new BABYLON.Vector3(15, 0, 0),
            Garry.getAbsolutePosition()
        );
    }
}else{
    window.location.reload();
}
});

window.addEventListener('keydown', (event) => {//Управление стрелкой
    if (state !== GAME_OVER){
    let x = event.keyCode;
    if (event.key == 'ArrowLeft') {
        Garry.physicsImpostor.applyImpulse(
            new BABYLON.Vector3(-15, 0, 0),
            Garry.getAbsolutePosition()
        );
    }
    let y = event.keyCode;
    if (event.key == 'ArrowRight') {
        Garry.physicsImpostor.applyImpulse(
            new BABYLON.Vector3(15, 0, 0),
            Garry.getAbsolutePosition()
        );
    }
}else{
    window.location.reload();
}
});
let speed = 7
window.addEventListener('keyup', () => {
    Garry.physicsImpostor.setLinearVelocity(new BABYLON.Vector3(0, 0, 10));
    if (score % 10 == 0) {
        speed = speed + 1;
    }
    Garry.physicsImpostor.setLinearVelocity(new BABYLON.Vector3(0, 0, speed));// Если очков больше 5 мяч ускоряется
    Garry.physicsImpostor.setAngularVelocity(new BABYLON.Vector3(0, 0, 0));
    console.log(speed);
});
window.addEventListener('beforeinstallprompt', (event) => {
    event.preventDefault();
}); 
const score=document.querySelector('.score');
const startScreen=document.querySelector('.startScreen');
const gameArea=document.querySelector('.gameArea');
const road = gameArea.getBoundingClientRect();
const rightMargin = 65;


/*console.log(gameArea);*/
startScreen.addEventListener('click',start);
let player={speed:5,score:0};
let keys ={ArrowUp:false,ArrowDown:false,ArrowLeft:false,ArrowRight:false}

// Sensores
const carpos = {x:0, y:0}
const collide_level = {top: 0, left:0, right:0, ts: 0}
const carmove = {moveleft: 0, moveright: 0}

const displayRefrest = Number(1000/frecuencia);

function keyDown(e){
    e.preventDefault();
    keys[e.key]=true;
}
function keyUp(e){
    e.preventDefault();
    keys[e.key]=false;
}
 //document.addEventListener('keydown',keyDown);
 //document.addEventListener('keyup',keyUp);

function isCollide2(a,b){
    aRect=a.getBoundingClientRect();
    bRect=b.getBoundingClientRect();
    return !((aRect.bottom<bRect.top)||(aRect.top>bRect.bottom)||(aRect.right<bRect.left)||(aRect.left>bRect.right))
}

function BoundingBox(x, y, height, width) {
    this.top = y;
    this.bottom = this.top + height;
    this.left = x;
    this.right = this.left + width;
}

function isCollide(a,b){
    aRect = new BoundingBox(a.x, a.y, 120, 50);
    bRect = new BoundingBox(b.x, b.y, 100, 50);
    return !((aRect.bottom<bRect.top)||(aRect.top>bRect.bottom)||(aRect.right<bRect.left)||(aRect.left>bRect.right))
}

function offsetCollide(car, enemy, axis, offset) {
    let collide_level = 0;
    for(const item of enemy) {
        const caroffset = {x: car.x, y: car.y};
        let new_top_collide = 0;
        for(let i=1; i<7; i++) {
            if(isCollide(caroffset, item)){
                new_top_collide = i;
                break;
            }
            caroffset[axis] += offset;
        }
        // If new collide is more critical, save it
        if(new_top_collide > 0 && (new_top_collide < collide_level || collide_level == 0)) {
            collide_level = new_top_collide;
            //console.log(`top collide ${collide_level}`)
            // if new collide is max, end forEach
            if(collide_level == 1) {
                break;
            }
        }
    };
    return collide_level;
}

function sensorPresencia(car, enemy) {

    let caroffset = {x: car.x, y: car.y};
    carpos.x = car.x;
    carpos.y = car.y;

    collide_level.top = offsetCollide(caroffset, enemy, "y", -120)

    if(car.x>0 ){
        caroffset = {x: car.x - 60, y: car.y};
        collide_level.left = offsetCollide(caroffset, enemy, "y", -120)    
    }
    else {
        collide_level.left = 1;
    }

    if(player.x<(road.width-rightMargin)){
        caroffset = {x: car.x + 60, y: car.y};
        collide_level.right = offsetCollide(caroffset, enemy, "y", -120)
    }
    else {
        collide_level.right = 1;
    }
    collide_level.ts++;
    console.log(collide_level)
    console.log(carmove)

    return collide_level
}

function moveLines(){
    let lines=document.querySelectorAll('.lines');
    lines.forEach(function(item){
        if(item.y >=650){
            item.y-=740;
        }
        item.y+=player.speed;
        item.style.top=item.y+"px";
    })
}
function endGame(won){
    player.start=false;
    startScreen.classList.remove('hide');
    if(won == true) {
        startScreen.innerHTML="<h2>¡Felicitaicones!</h2> Puntaje:"+player.score+" "+"<br>Presione para volver a empezar";
    } else {
        startScreen.innerHTML="<h2>Game Over</h2> Puntaje:"+player.score+" "+"<br>Presione para volver a empezar";
    }
    collide_level.top = 0;
    collide_level.left = 0;
    collide_level.right = 0;
    collide_level.ts = 0;
}
function moveEnemy(car){
    let enemy=document.querySelectorAll('.enemy');

    sensorPresencia(car, enemy);

    enemy.forEach(function(item){
        
        if(isCollide(car,item)){
            console.log("Bang!");
            endGame(false);
        }
        if(item.y >=750){
            item.y=-300;
            //item.x = Math.floor(Math.random()*350);
            const carril = Math.round(1+Math.random()*2);
            if(carril == 1) {
                item.x = 0;
            }
            if(carril == 2) {
                item.x = 65;
            }
            if(carril == 3) {
                item.x = 130;
            }
            item.style.left = item.x+"px";
            
        }
        item.y+=player.speed;
        item.style.top=item.y+"px";
    })
}
function gamePlay(){
    let car=document.querySelector('.car');

    car.y = player.y;
    car.x = player.x;
    /*console.log(road);*/
    if(player.start){
        moveLines();
        moveEnemy(car);

        /*if(keys.ArrowUp && player.y>(road.top+70)){
            player.y-=player.speed
        }
        if(keys.ArrowDown && player.y<(road.bottom-85)){
            player.y+=player.speed
        }
        if(keys.ArrowLeft && player.x>0 ){
            player.x-=player.speed
        }
        if(keys.ArrowRight && player.x<(road.width-70)){
            player.x+=player.speed
        }*/
        if(carmove.moveleft && player.x>0 ){
            player.x-=player.speed
        }
        if(carmove.moveright && player.x<(road.width-rightMargin)){
            player.x+=player.speed
        }
        car.style.top=player.y+"px";
        car.style.left=player.x+"px";
        player.score++;
        let ps=player.score-1;
        score.innerText="Puntos "+ps;

        if(ps >= 2000) {
            endGame(true);
        }

        //window.requestAnimationFrame(gamePlay);
        setTimeout( gamePlay, displayRefrest );
    }
}
function start(){
    //gameArea.classList.remove('hide');
    startScreen.classList.add('hide');
    gameArea.innerHTML="";
    player.start=true;
    player.score=0;
    window.requestAnimationFrame(gamePlay);

    for(x=0;x<5;x++){
        let roadLine=document.createElement('div');
        roadLine.setAttribute('class','lines');
        roadLine.y=(x*150);
        roadLine.style.top=roadLine.y+"px";
        gameArea.appendChild(roadLine);
    }

    let car=document.createElement('div');
    car.setAttribute('class','car');

    gameArea.appendChild(car);

    player.x=car.offsetLeft;
    player.y=car.offsetTop;



    for(x=0;x<3;x++){
        let enemyCar=document.createElement('div');
        enemyCar.setAttribute('class','enemy');
        enemyCar.y=((x+1)*350)*-1;
        const carril = Math.floor(1+Math.random()*2);
        if(carril == 1) {
            enemyCar.x = 0;
        }
        if(carril == 2) {
            enemyCar.x = 65;
        }
        if(carril == 3) {
            enemyCar.x = 115;
        }
        //enemyCar.x = Math.floor(Math.random()*350);
        enemyCar.style.top=enemyCar.y+"px";
        enemyCar.style.left=enemyCar.x+"px";
        enemyCar.style.backgroundColor=randomColor();        
        gameArea.appendChild(enemyCar);
    }


}
function randomColor(){
    function c(){
        let hex=Math.floor(Math.random()*256).toString(16);
        return ("0"+String(hex)).substr(-2);
    }
    return "#"+c()+c()+c();
}

async function update() {
    const data = {
        //carpos: carpos,
        collide_level: collide_level,
    }
    
    const resp = await fetch("/gui", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    
    if(resp.ok) {
        const resp_data = await resp.json();
        carmove.moveleft = resp_data.moveleft;
        carmove.moveright = resp_data.moveright;
    }
}


(function my_func() {
    update();
    setTimeout( my_func, 1000/frecuencia );
})();
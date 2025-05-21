function formatDate(date) {
    const pad = (n) => n.toString().padStart(2, '0');
    return date.getFullYear() + '-' +
        pad(date.getMonth() + 1) + '-' +
        pad(date.getDate()) + ' ' +
        pad(date.getHours()) + ':' +
        pad(date.getMinutes()) + ':' +
        pad(date.getSeconds());
}
// $.log("RenewStart " + formatDate(new Date()));

function formatDateTime(date) {
    const pad = (n) => n.toString().padStart(2, '0');
    return pad(date.getHours()) + ':' +
        pad(date.getMinutes()) + ':' +
        pad(date.getSeconds()) + ' ' ;
}

class Cube {
    constructor(cubeName) {
        this.cubeName = cubeName;
        this.subNode = $.subNode(cubeName);
        this.vector = new Vector3(0, 0, 0);
        this.posMaxIdx = 27;
        this.setNewPosIdx(Math.floor(Math.random() * this.posMaxIdx));
    }
    setNewPosIdx(idx){ // 表示位置を設定
        this.posOldidx = this.posidx;
        this.posOldX = this.posX;
        this.posOldY = this.posY;
        this.posOldZ = this.posZ;
        this.posidx = idx;
        const [x, y, z] = this.idx2xyz(this.posidx);
        this.posX = x;
        this.posY = y;
        this.posZ = z;
        this.moveCount = 0; // 移動開始
    }
    setPosition(){ // 表示位置を一気に移動
        const posx = this.posX / 3 - (1/3);
        const posy = this.posY / 3 + (1/3/2);
        const posz = this.posZ / 3 - (1/3);
        this.vector.set(posx, posy, posz);
        this.subNode.setPosition(this.vector);
        this.moveCount = 1; // 移動完了
    }
    setWaitTime(){
        //this.waittime = Math.floor(Math.random() * 4000) + 1000; // 1〜5秒（ms）
        this.waittime = Math.floor(Math.random() * 7000) + 3000; // 3〜10秒（ms）
        //this.waittime = 1000; // 1秒（ms）
        //this.waittime = 10; // 0.01秒（ms）debug
        this.waitstartTime = Date.now(); // 現在の時刻（ms）
        //$.log(formatDateTime(new Date()) + " 待機時間設定 " + (this.waittime / 1000) + "s " + this.cubeName);
    }
    update(cubes){
        if(this.moveCount < 1){
            // 移動中
            this.movePosition();
            if( this.moveCount >= 1 ){
                this.setPosition(); // 表示位置を設定
                cubes.NextMoveCube_Random(); // ランダムに次のキューブを探す
                return;
            }
            return;
        }
        if (!this.waittime) {return} // 待機時間が設定されていない場合は何もしない
        if (Date.now() - this.waitstartTime < this.waittime) {return} // 待機時間経過確認
        this.waittime = 0;

        // 待機時間が経過したら実行する処理
        //$.log(formatDateTime(new Date()) + " 待機時間経過");

        this.setDestinationPosIdx(cubes); // 移動先の位置を設定

    }
    setDestinationPosIdx(cubes){ // 移動先の位置を設定
        const MoveList = [];
        const directions = [
            [1, 0, 0], [-1, 0, 0],
            [0, 1, 0], [0, -1, 0],
            [0, 0, 1], [0, 0, -1]
        ];
        for (const [dx, dy, dz] of directions) {
            const nx = this.posX + dx;
            const ny = this.posY + dy;
            const nz = this.posZ + dz;
            if (nx >= 0 && nx < 3 && ny >= 0 && ny < 3 && nz >= 0 && nz < 3) {
                const newIdx = this.xyz2idx(nx, ny, nz);
                if (!cubes.cubes.some(c => c !== this && c.posidx === newIdx )) {
                    //break; // debug
                    MoveList.push(newIdx);
                }
            }
        }
        // 移動元は含めない
        // 移動できる方向がなかったら次のキューブへ
        if (MoveList.length === 0) {
            //$.log(formatDateTime(new Date()) + " 移動できる方向が無いので次のキューブへ");
            //this.setPosition(); // 表示位置を設定
            //this.NextSerchObj();
            cubes.NextMoveCube_Random(); // ランダムに次のキューブを探す
            return;
        }

        // １ブロック移動開始
        const randomNewIdx = MoveList[Math.floor(Math.random() * MoveList.length)];
        this.setNewPosIdx(randomNewIdx);
        //this.setPosition();

    }
    movePosition(){
        //$.log(formatDateTime(new Date()) + " movePosition() " + this.moveCount);
        this.moveCount += 0.001; // 移動中
        //this.moveCount += 1; // debug
        if( this.moveCount >= 1 ){
            return;
        }
        const posx = (this.posOldX + ((this.posX - this.posOldX) * this.moveCount)) / 3 - (1/3);
        const posy = (this.posOldY + ((this.posY - this.posOldY) * this.moveCount)) / 3 + (1/3/2);
        const posz = (this.posOldZ + ((this.posZ - this.posOldZ) * this.moveCount)) / 3 - (1/3);
        this.vector.set(posx, posy, posz);
        this.subNode.setPosition(this.vector);
    }
    idx2xyz(idx){
        const x = idx % 3;
        const y = Math.floor((idx % 9) / 3);
        const z = Math.floor(idx / 9);
        return [x, y, z];
    }
    xyz2idx(x,y,z){
        const idx = x + y * 3 + z * 9;
        return idx;
    }
}

class Cubes {
    constructor() {
        const cubes = [];
        const cube_names = ["Cube000","Cube001","Cube010","Cube011","Cube100","Cube101","Cube110","Cube111"];
        //const cube_names = ["Cube010","Cube011","Cube100","Cube101","Cube110","Cube111"];
        //const cube_names = ["Cube001","Cube010","Cube011","Cube100","Cube101","Cube110","Cube111"];
        for (let cube_name of cube_names) {
           //$.log(cube_name);
           cubes.push(new Cube(cube_name));
        }
        this.cubes = cubes;
    }
    setAllPosition(){ // 表示位置を一気に移動
        for (let cube_obj of this.cubes) {
            cube_obj.setPosition();
        }
    }
    removeDuplicatePositions() { // 場所の重複を排除
        const cubes = this.cubes;
        for (let cube_obj of cubes) {
            if (!cubes.some(c => c !== cube_obj && c.posidx === cube_obj.posidx)) continue;
            // 場所が被ってる
            //$.log(cube_obj.cubeName + ":" + cube_obj.posX + "," + cube_obj.posY + "," + cube_obj.posZ);
            // 重複しているので、空いている位置を探す
            for (let i = 1; i < cube_obj.posMaxIdx; i++) {
                let candidateIdx = cube_obj.posidx + i;
                if (candidateIdx >= cube_obj.posMaxIdx) {
                    // 位置が最大値を超えた場合、最初から探す
                    //$.log("超えた:" + candidateIdx + " " + (candidateIdx - cube_obj.posMaxIdx));
                    candidateIdx -= cube_obj.posMaxIdx;
                }
                // 空いている場所を探す
                const isSpace = !cubes.some(c => c !== cube_obj && c.posidx === candidateIdx);
                if (isSpace) {
                    cube_obj.setNewPosIdx(candidateIdx); // 表示位置を設定
                    break;
                }
            }
        }
    }
    NextMoveCube_Random(){ // ランダムに次のキューブを探す
        const cubes = this.cubes;
        this.nextMoveCube = cubes[Math.floor(Math.random() * cubes.length)];
        //$.log("NextMoveCube_Random() " + this.nextMoveCube.cubeName);
        this.nextMoveCube.setWaitTime(); // 待機時間を設定
    }
    update(){
        const cubes = this.cubes;
        for (let cube_obj of cubes) {
            cube_obj.update(this);
        }
    }
}
const cubes = new Cubes();

// 初期実行用
class AutoExec {
    constructor() {
        this.IsFirst = true;
    }
    exec(){
        if( this.IsFirst == false){
            return;
        }
        this.IsFirst = false;
        //$.log("autoExec.exec()");
        cubes.removeDuplicatePositions(); // 場所の重複を排除
        cubes.setAllPosition(); // 表示位置を一気に移動
        cubes.NextMoveCube_Random(); // ランダムに次のキューブを探す
    }
}
const autoExec = new AutoExec();

// 動作確認用サンプル
let count = 0;
let move_speed = 0;
function sampleMove(){
    if( count >= 1 ){
        move_speed = -0.01;
    }
    if( count <= 0 ){
        move_speed = 0.01;
    }
    count+=move_speed;
    const shortHandNodeX = $.subNode("Cube000");
    const Wrkpos = new Vector3(0,count,count);
    shortHandNodeX.setPosition(Wrkpos);
}

$.onUpdate(deltaTime => {
    // 動作確認用サンプル
    //sampleMove();

    autoExec.exec(cubes);
    cubes.update();

});

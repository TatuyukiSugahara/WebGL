//URL : https://wgld.org/sitemap.html

onload = function()
{
    //canvasエレメント取得。
    var c = document.getElementById('canvas');
    c.width = 500;
    c.height = 300;
    //webglコンテキスト取得。
    var gl = c.getContext('webgl') || c.getContext('experimental-webgl');
     //頂点シェーダ。
    var v_shader = create_shader('vs');
    //フラグメントシェーダ。
    var f_shader = create_shader('fs');
    //プログラムオブジェクト。
    var prg = create_program(v_shader, f_shader);
    //attributelocation。
    var attLocation = new Array();
	attLocation[0] = gl.getAttribLocation(prg, 'position');
	attLocation[1] = gl.getAttribLocation(prg, 'normal');
    attLocation[2] = gl.getAttribLocation(prg, 'color');
	
    //要素数。
    var attStride = new Array();
	attStride[0] = 3;
	attStride[1] = 3;
	attStride[2] = 4;
   
    //トーラス。
    var torusData = torus(32, 32, 1.0, 2.0);
	var position = torusData[0];
	var normal = torusData[1];
	var color = torusData[2];
	var index = torusData[3];

    //vbo
    var position_vbo = create_vbo(position);
    var normal_vbo = create_vbo(normal);
    var color_vbo = create_vbo(color);
    
    //vbo登録。
    set_attribute([position_vbo,normal_vbo,color_vbo],attLocation,attStride);
    //ibo登録。
    var ibo = create_ibo(index);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,ibo);

    //取得。
    var uniLocation = new Array();
    uniLocation[0] = gl.getUniformLocation(prg,'mvpMatrix');
    uniLocation[1] = gl.getUniformLocation(prg,'invMatrix');
    uniLocation[2] = gl.getUniformLocation(prg,'lightDir');
    uniLocation[3] = gl.getUniformLocation(prg, 'eyedir');
    uniLocation[4] = gl.getUniformLocation(prg, 'ambientcolor');


    //matIV。
    var m = new matIV();
    //行列作成。
    var mMatrix = m.identity(m.create());
    var vMatrix = m.identity(m.create());
    var pMatrix = m.identity(m.create());
    var tmpMatrix = m.identity(m.create());
    var mvpMatrix = m.identity(m.create());
    var invMatrix = m.identity(m.create());
    //ビュー行列。
    m.lookAt([0.0, 0.0, 20.0], [0, 0, 0], [0, 1, 0], vMatrix);
    //プロジェクション行列。
    m.perspective(45, c.width / c.height, 0.1, 100, pMatrix);
    //座標変換。
    m.multiply(pMatrix, vMatrix, tmpMatrix);

    //ライトの向き。
    var lightDir = [-0.5,0.5,0.5];
    //視線。
    var eyeDir = [0.0,0.0,1.0];
    //環境光カラー。
    var ambient = [0.3,0.1,0.1,1.0];

    // カウンタの宣言
    var count = 0;
    //深度テスト。
    gl.enable(gl.DEPTH_TEST);
	gl.depthFunc(gl.LEQUAL);
	gl.enable(gl.CULL_FACE);
    //ループ。
    (function(){
        //canvas初期化。
        gl.clearColor(0.0, 0.0, 0.0, 1.0);
        gl.clearDepth(1.0);
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
        
        //カウンタ加算。
        count++;
        
        //カウンタからラジアンを算出。
        var rad = (count % 360) * Math.PI / 180;
        
        //モデル座標変換行列作成。
        //Y軸に回転させる。
        m.identity(mMatrix);
        m.rotate(mMatrix, rad, [0, 1, 1], mMatrix);
        m.multiply(tmpMatrix, mMatrix, mvpMatrix);

        //逆行列作成。
        m.inverse(mMatrix,invMatrix);

        //登録。
        gl.uniformMatrix4fv(uniLocation[0], false, mvpMatrix);
		gl.uniformMatrix4fv(uniLocation[1], false, invMatrix);
        gl.uniform3fv(uniLocation[2], lightDir);
        gl.uniform3fv(uniLocation[3], eyeDir);
        gl.uniform4fv(uniLocation[4], ambient);

        //インデックスを使用し描画命令。
        gl.drawElements(gl.TRIANGLES, index.length, gl.UNSIGNED_SHORT, 0);
        
        gl.flush();
        
        //ループのために再帰呼び出し。
        setTimeout(arguments.callee, 1000 / 30);
    })();

    //シェーダー生成。
    function create_shader(id){
        //変数。
        var shader;
        //タグへの参照。
        var scriptElement = document.getElementById(id);
        //タグがない場合。
        if(!scriptElement){return;}
        //属性チェック。
        switch(scriptElement.type){
            //頂点シェーダ。
            case 'x-shader/x-vertex':
                shader = gl.createShader(gl.VERTEX_SHADER);
                break;
            //フラグメントシェーダ。
            case 'x-shader/x-fragment':
                shader = gl.createShader(gl.FRAGMENT_SHADER);
                break;
            default :
                return;
        }
        //生成されたシェーダを割り当て。
        gl.shaderSource(shader, scriptElement.text);
        //コンパイル。
        gl.compileShader(shader);
        //チェック。
        if(gl.getShaderParameter(shader, gl.COMPILE_STATUS)){
            //シェーダ返却。
            return shader;
        }else{
            //失敗。
            alert(gl.getShaderInfoLog(shader));
        }
    }
    //プログラムオブジェクト生成。
    function create_program(vs, fs)
    {
        //プログラムオブジェクト生成。
        var program = gl.createProgram();
        //シェーダ割り当て。
        gl.attachShader(program, vs);
        gl.attachShader(program, fs);
        //リンク。
        gl.linkProgram(program);
        //チェック。
        if(gl.getProgramParameter(program, gl.LINK_STATUS)){
            //有効。
            gl.useProgram(program);
            //返却。
            return program;
        }else{
            //失敗。
            alert(gl.getProgramInfoLog(program));
        }
    }
    
    //VBO。
    function create_vbo(data)
    {
        //バッファオブジェクト生成。
        var vbo = gl.createBuffer();
        //バインド。
        gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
        //データ設定。
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data), gl.STATIC_DRAW);
        //バインド解除。
        gl.bindBuffer(gl.ARRAY_BUFFER, null);
        //返却。
        return vbo;
    }

    //IBO。
    function create_ibo(data)
    {
        //バッファオブジェクト。
        var ibo = gl.createBuffer();
        //バインド。
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,ibo);
        //データ設定。
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Int16Array(data),gl.STATIC_DRAW);
        //バインド解除。
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,null);
        //返却。
        return ibo;
    }

    //バインドし登録する。
    function set_attribute(vbo,attl,atts)
    {
        //配列を処理。
        for(var i in vbo)
        {
            //バッファをバインド。
            gl.bindBuffer(gl.ARRAY_BUFFER,vbo[i]);
            //有効に。
            gl.enableVertexAttribArray(attl[i]);
            //登録。
            gl.vertexAttribPointer(attl[i],atts[i],gl.FLOAT,false,0,0);
        }
    }
    //トーラスモデル。
    //ドーナツ型。
    function torus(row,column,irad,orad)
    {
        var pos = new Array(), nor = new Array(),
        col = new Array(), idx = new Array();
        for(var i = 0; i <= row; i++){
            var r = Math.PI * 2 / row * i;
            var rr = Math.cos(r);
            var ry = Math.sin(r);
            for(var ii = 0; ii <= column; ii++){
                var tr = Math.PI * 2 / column * ii;
                var tx = (rr * irad + orad) * Math.cos(tr);
                var ty = ry * irad;
                var tz = (rr * irad + orad) * Math.sin(tr);
                var rx = rr * Math.cos(tr);
                var rz = rr * Math.sin(tr);
                pos.push(tx, ty, tz);
                nor.push(rx, ry, rz);
                var tc = hsva(360 / column * ii, 1, 1, 1);
                col.push(tc[0], tc[1], tc[2], tc[3]);
            }
        }
        for(i = 0; i < row; i++){
            for(ii = 0; ii < column; ii++){
                r = (column + 1) * i + ii;
                idx.push(r, r + column + 1, r + 1);
                idx.push(r + column + 1, r + column + 2, r + 1);
            }
        }
        return [pos, nor, col, idx];
    }
    //RGB変換。
    function hsva(h,s,v,a)
    {
        if(s > 1 || v > 1 || a > 1){return;}
		var th = h % 360;
		var i = Math.floor(th / 60);
		var f = th / 60 - i;
		var m = v * (1 - s);
		var n = v * (1 - s * f);
		var k = v * (1 - s * (1 - f));
		var color = new Array();
		if(!s > 0 && !s < 0){
			color.push(v, v, v, a); 
		} else {
			var r = new Array(v, n, m, m, k, v);
			var g = new Array(k, v, v, n, m, m);
			var b = new Array(m, m, k, v, v, n);
			color.push(r[i], g[i], b[i], a);
		}
		return color;
    }
};
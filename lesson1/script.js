onload = function(){
    // canvas�G�������g���擾
    var c = document.getElementById('canvas');
    c.width = 500;
    c.height = 300;

    // webgl�R���e�L�X�g���擾
    var gl = c.getContext('webgl') || c.getContext('experimental-webgl');

    // canvas�����ŃN���A(������)����
    gl.clearColor(0.0, 0.0, 0.0, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT);
};
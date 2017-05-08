///phantomjs phantom_req.js http://www.xdaili.cn/freeproxy.html

//console.log(getNowFormatDate());

var page = require('webpage').create(),
    system = require('system'),
    address;
address = system.args[1];

function getNowFormatDate() {
    var date = new Date();
    var seperator1 = '-';
    var seperator2 = ':';

    var month = ('0' + (date.getMonth() + 1)).substr(-2);
    var day = ('0' + date.getDate()).substr(-2);
    var hour = ('0' + date.getHours()).substr(-2);
    var minute = ('0' + date.getMinutes()).substr(-2);
    var second = ('0' + date.getSeconds()).substr(-2);

    var currentdate = date.getFullYear() + seperator1 + month + seperator1 + day +
        ' ' + hour + seperator2 + minute + seperator2 + second;
    return currentdate;
}

function daili() {
    //console.log(getNowFormatDate());
    // init and settings
    page.settings.resourceTimeout = 30000;
    page.settings.XSSAuditingEnable = true;
    //page.viewportSize = { width: 1000, height: 1000 };
    page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36';
    page.customHeaders = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    };
    page.open(address, function() {
        //console.log(address);
        //console.log('begin');
    });

    page.onLoadFinished = function(status) {
        //console.log('Status: ' + status);
        console.log(page.content);
        //console.log(getNowFormatDate());
        phantom.exit();
    };
}

function cuiqingcai() {
    address = 'http://cuiqingcai.com';
    console.log(getNowFormatDate());
    page.open(address, function(status) {
        console.log('Status: ' + status);
        if (status === 'success') {
            page.render('example.png');
        }
        console.log(getNowFormatDate());
        phantom.exit();
    });
}

if (address === '') {
    cuiqingcai();
} else {
    daili();
}
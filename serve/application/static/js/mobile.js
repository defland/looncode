// 判断如果是移动端浏览器，就自动访问m页面
function uaredirect(murl){
    try {
        if(document.getElementById("bdmark") != null){
            return;
        }
        var urlhash = window.location.hash;
        if (!urlhash.match("fromapp")){
            if ((navigator.userAgent.match(/(iPhone|iPod|Android|ios|iPad)/i))) {
            location.replace(murl);
            }
        }
    } catch(err){}
}
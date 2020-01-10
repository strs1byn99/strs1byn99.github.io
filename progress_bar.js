var element801 = document.getElementById("logo801");
var element802 = document.getElementById("logo802");
var element701 = document.getElementById("logo701");
var element702 = document.getElementById("logo702");
var element601 = document.getElementById("logo601");
var element501 = document.getElementById("logo501");
var element502 = document.getElementById("logo502");
skills(element801, "skill80");
skills(element802, "skill80");
skills(element701, "skill70");
skills(element702, "skill70");
skills(element601, "skill60");
skills(element501, "skill50");
skills(element502, "skill50");
function skills(element, skill) {
    var co = 0;
    var observer = new IntersectionObserver(function(entries) {
        if(entries[0].isIntersecting === true && co < 2)
            element.classList.remove(skill);
            element.offsetWidth=element.offsetWidth;
            element.classList.add(skill);
            co = co+1;
    }, { threshold: [0] });
    observer.observe(element);
}
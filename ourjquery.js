window.onload = function(){hide_all(); };
function forget()
{
    var obj = document.getElementById('forget');

    if (obj.style.display =='none')
    {
        obj.style.display = 'block';
    }
    else{
        obj.style.display = 'none';
    }
}
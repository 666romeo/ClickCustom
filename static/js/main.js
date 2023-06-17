
if (window.NodeList && !NodeList.prototype.forEach) {
    NodeList.prototype.forEach = function (callback, thisArg) {
        thisArg = thisArg || window;
        for (var i = 0; i < this.length; i++) {
            callback.call(thisArg, this[i], i, this);
        }
    };
}


document.querySelectorAll('.dropdown').forEach(function (dropDownWrapper) {
    const dropDownBtn = dropDownWrapper.querySelector('.dropdown__button');
    const dropDownList = dropDownWrapper.querySelector('.dropdown__list');

    const dropDown = document.querySelector('.dropdown')
    const dropDowns = dropDown.querySelectorAll('.dropdown');
    const dropDownListItems = dropDownList.querySelectorAll('.dropdown__list-item');

    dropDownBtn.addEventListener('click', function () {
        dropDownList.classList.toggle('dropdown__list--visible');
        dropDown.classList.toggle('dropdown--active');
    });

    dropDownListItems.forEach(function (listItem) {
        listItem.addEventListener('click', function (e) {
            dropDownBtn.innerText = this.innerText;
            dropDownList.classList.remove('dropdown__list--visible');
            dropDown.classList.remove('dropdown--active');
        });
    });

    document.addEventListener('click', function (e) {
        if ( e.target !== dropDownBtn ) {
            dropDownBtn.classList.remove('dropdown__list--active');
            dropDownList.classList.remove('dropdown__list--visible');
            dropDown.classList.remove('dropdown--active');
        }
    });

    document.addEventListener('keydown', function (e) {
        if ( e.key === 'Tab' || e.key === 'Escape' ) {
            dropDownBtn.classList.remove('dropdown__list--active');
            dropDownList.classList.remove('dropdown__list--visible');
            dropDown.classList.remove('dropdown--active');
        }
    });

    dropDown.addEventListener("mouseover", function () {
        $(".dropdown__list").addClass("dropdown__list--visible");
        dropDown.classList.toggle('dropdown--active');
    });
    dropDown.addEventListener("mouseout", function(){
        $(".dropdown__list").removeClass("dropdown__list--visible");
        dropDown.classList.remove('dropdown--active');
    });
});
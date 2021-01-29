//bugs
//minimum numbers are not accounted for when figuring out the size and offset off numbers in mobile mode

"use strict";

var header = document.getElementById('header');
var main = document.getElementById('main');
var numbers = document.getElementById('numbers');
var side = document.getElementById('side');
var timer = document.getElementById('timer');

var windowHeight = window.innerHeight;
var windowWidth = window.innerWidth;
var lineHeight = 14;
var marginThickness = 10;

function set_height(element, amount){
    element.style.height = String(amount) + 'px';
}

function set_width(element, amount) {
    element.style.width = String(amount) + 'px';
}

//used for calculating the numbers text as if main text rolls over to the nextline there needs to be a newline char
function chars_per_line(lineLength) {
    var div = document.createElement('div');
    div.style.fontFamily = 'monospace';
    div.style.display = 'inline';
    document.body.appendChild(div);
    var text = '';
    while (div.offsetWidth < lineLength) {
        text += 'a';
        div.textContent = text;
    }
    div.parentNode.removeChild(div);
    return text.length - 1;
}

function add_numbers() {
    var numbersText = '';
    var lineLength = main.offsetWidth - marginThickness;
    var plainText = main.textContent;
    var mainText = plainText.split('\n');
    if (mainText[0] == '') {mainText = [plainText];}
    if (mainText[0] == '') {mainText = [];}
    var lineNum = 0;
    var totalLines = 0;
    var minimumLines = Math.floor((main.offsetHeight - marginThickness) / lineHeight);

    var charsPerLine = chars_per_line(lineLength);

    for (; lineNum < mainText.length; ++lineNum) {
        numbersText += String(lineNum + 1) + '\n';
        ++totalLines;

        var linesTaken = Math.ceil(mainText[lineNum].length / charsPerLine);
        for (var _ = 1; _ < linesTaken; ++_) {
            numbersText += '\n';
            ++totalLines;
        }
    }

    for (; totalLines < minimumLines; ++totalLines) {
        numbersText += String(lineNum + 1) + '\n';
        ++lineNum;
    }
    
    numbers.textContent = numbersText.substring(0, numbersText.length - 1);
}

function get_scrollbar_width() {
    var outer = document.createElement('div');
    outer.style.visibility = 'hidden';
    outer.style.overflow = 'scroll';
    outer.style.msOverflowStyle = 'scrollbar';
    document.body.appendChild(outer);
    var inner = document.createElement('div');
    outer.appendChild(inner);
    var scrollbarWidth = (outer.offsetWidth - inner.offsetWidth);
    outer.parentNode.removeChild(outer);
    return scrollbarWidth;
}

var headerHeight;
if (header.textContent == '') {
    header.parentNode.removeChild(header);
    headerHeight = 0;
} else {
    headerHeight = header.offsetHeight;
}

//sets up different webpage if the viewport is small, this is to make decent mobile viewing experiances
if (windowWidth < 1000) {
    side.parentNode.removeChild(side);

    //put the largest number in numbers then calculate the width
    numbers.textContent = String(main.textContent.split('\n').length);
    var numbersWidth = numbers.offsetWidth;

    //set width of main and find mainHeight, scrollbarwidth is discluded origonally to see if it fits witout it
    set_width(main, windowWidth - numbersWidth);
    var mainHeight = windowHeight - headerHeight;
    if (main.offsetHeight > mainHeight) {
        mainHeight = main.offsetHeight;
        set_width(main, windowWidth - numbersWidth - get_scrollbar_width());
    }

    //set height of main and numbers
    set_height(main, mainHeight);
    set_height(numbers, mainHeight);

    add_numbers();

    //offset main
    main.style.left = String(numbersWidth) + 'px';
} else {
    //add min width of 4 digits to numbers
    numbers.style.minWidth = '43px';

    //put the largest number in numbers then calculate the width
    numbers.textContent = String(main.textContent.split('\n').length);
    var numbersWidth = numbers.offsetWidth;

    var sideWidth = side.offsetWidth;

    //set width of main and find mainHeight, scrollbarwidth is discluded origonally to see if it fits witout it
    set_width(main, windowWidth - numbersWidth - sideWidth);
    var mainHeight = windowHeight - headerHeight;
    var potentialHeight = Math.max(main.offsetHeight, side.offsetHeight);
    if (potentialHeight > mainHeight) {
        mainHeight = potentialHeight;
        set_width(main, windowWidth - numbersWidth - sideWidth - get_scrollbar_width());
    }

    //set height of main and numbers
    set_height(main, mainHeight);
    set_height(numbers, mainHeight);
    
    add_numbers();

    //position main in the webpage
    main.style.left = String(numbersWidth) + 'px';

    //set height of side
    var sideHeight = Math.min(windowHeight, mainHeight);
    set_height(side, sideHeight);

    //start webpage expiry timer
    var timeCreated = document.querySelector('meta[name="timeCreated"]').content / 60;
    var currTime = new Date().getTime() / 60000;
    var minsRemaining = Math.max(0, Math.floor(60 - (currTime - timeCreated)));
    timer.textContent = 'time till webpage expires: ' + String(Math.max(0, minsRemaining)) + ' minutes';
    if (minsRemaining != 0) {
        setInterval(function() {
            minsRemaining -= 1;
            timer.textContent = 'time till webpage expires: ' + String(Math.max(0, minsRemaining)) + ' minutes';
        }, 60000);
    }

    //makes side panel stop scrolling down once the header is not visible, if there is no header event listener isn't used
    if (headerHeight) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > headerHeight) {
                side.style.position = 'fixed';
                side.style.top = '0px';
            } else {
                side.style.position = 'absolute';
                side.style.top = String(headerHeight) + 'px';
            }
        });
    } else {
        side.style.position = 'fixed';
    }
}

window.addEventListener('resize', function () {
    window.location.href = window.location.href;
});

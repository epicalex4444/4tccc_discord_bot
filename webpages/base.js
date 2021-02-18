"use strict";

const header = document.getElementById('header');
const main = document.getElementById('main');
const numbers = document.getElementById('numbers');
const lineHeight = 14;
const marginThickness = 10;

//remove header if it as no text, headerHeight is also set corrsespondingly
let headerHeight;
if (header.textContent == '') {
    header.parentNode.removeChild(header);
    headerHeight = 0;
    document.getElementById('side').style.position = 'fixed';
} else {
    headerHeight = header.offsetHeight;
}

function set_height(element, amount){
    element.style.height = String(amount) + 'px';
}

function set_width(element, amount) {
    element.style.width = String(amount) + 'px';
}

function get_scrollbar_width() {
    const outer = document.createElement('div');
    outer.style.visibility = 'hidden';
    outer.style.overflow = 'scroll';
    outer.style.msOverflowStyle = 'scrollbar';
    document.body.appendChild(outer);
    const inner = document.createElement('div');
    outer.appendChild(inner);
    const scrollbarWidth = outer.offsetWidth - inner.offsetWidth;
    outer.parentNode.removeChild(outer);
    return scrollbarWidth;
}

function add_numbers() {
    function chars_per_line(lineLength) {
        const div = document.createElement('div');
        div.style.fontFamily = 'monospace';
        div.style.display = 'inline';
        document.body.appendChild(div);
        let text = '';
        while (div.offsetWidth < lineLength) {
            text += 'a';
            div.textContent = text;
        }
        div.parentNode.removeChild(div);
        return text.length - 1;
    }

    let numbersText = '';
    const lineLength = main.offsetWidth - marginThickness;
    const plainText = main.textContent;
    let mainText = plainText.split('\n');
    if (mainText[0] == '') {mainText = [plainText];}
    if (mainText[0] == '') {mainText = [];}
    let lineNum = 0;
    let totalLines = 0;
    const minimumLines = Math.floor((main.offsetHeight - marginThickness) / lineHeight);

    const charsPerLine = chars_per_line(lineLength);

    for (; lineNum < mainText.length; ++lineNum) {
        numbersText += String(lineNum + 1) + '\n';
        ++totalLines;

        const linesTaken = Math.ceil(mainText[lineNum].length / charsPerLine);
        for (let _ = 1; _ < linesTaken; ++_) {
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

//is mobile just mean small viewport
function is_mobile() {
    return window.innerWidth < 1000;
}

//put the largest number in numbers to calculate the width
function get_numbers_width() {
    numbers.textContent = String(main.textContent.split('\n').length);
    return numbers.offsetWidth;
}

function setup_webpage(mobile) {
    //sets up different webpage if the viewport is small, this is to make decent mobile viewing experiances
    if (mobile) {
        const numbersWidth = get_numbers_width();

        //set width of main and find mainHeight, scrollbarwidth is discluded origonally to see if it fits witout it
        set_width(main, window.innerWidth - numbersWidth);
        let mainHeight = window.innerHeight - headerHeight;
        if (main.offsetHeight > mainHeight) {
            mainHeight = main.offsetHeight;
            set_width(main, window.innerWidth - numbersWidth - get_scrollbar_width());
        }

        //set height of main and numbers
        set_height(main, mainHeight);
        set_height(numbers, mainHeight);

        add_numbers();

        //position main section
        main.style.left = String(numbersWidth) + 'px';
    } else {
        const side = document.getElementById('side');

        //add min width of 4 digits to numbers
        numbers.style.minWidth = '43px';

        const numbersWidth = get_numbers_width();
        const sideWidth = side.offsetWidth;

        //set width of main and find mainHeight, scrollbarwidth is discluded origonally to see if it fits without it
        set_width(main, window.innerWidth - numbersWidth - sideWidth);
        let mainHeight = window.innerHeight - headerHeight;
        const potentialHeight = Math.max(main.offsetHeight, side.offsetHeight);
        if (potentialHeight > mainHeight) {
            mainHeight = potentialHeight;
            set_width(main, window.innerWidth - numbersWidth - sideWidth - get_scrollbar_width());
        }

        //set height of main and numbers
        set_height(main, mainHeight);
        set_height(numbers, mainHeight);
    
        add_numbers();

        //position main section
        main.style.left = String(numbersWidth) + 'px';

        //set height of side
        const sideHeight = Math.min(window.innerHeight, mainHeight);
        set_height(side, sideHeight);
    }
}

function setup_side() {
    const side = document.getElementById('side');

    //start webpage expiry timer
    const timeCreated = 1612336528 / 60; //mins
    const currTime = new Date().getTime() / 60000; //mins
    let timeRemaining = Math.ceil(1440 - (currTime - timeCreated));
    let hours = Math.max(0, Math.floor(timeRemaining / 60));
    let mins = Math.max(0, timeRemaining - hours * 60);
    document.getElementById('timer').textContent = 'time till webpage expires:\n' + String(hours) + 'h, ' + String(mins) + 'm';

    if (timeRemaining != 0) {
        setInterval(function() {
            timeRemaining -= 1;
            hours = Math.max(0, Math.floor(timeRemaining / 60));
            mins = Math.max(0, timeRemaining - hours * 60);
            document.getElementById('timer').textContent = 'time till webpage expires:\n' + String(hours) + 'h, ' + String(mins) + 'm';
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

    //needs to be done if the webpage is already scrolled down when the webpage is setup
    if (window.scrollY > headerHeight) {
        side.style.position = 'fixed';
        side.style.top = '0px';
    }
}

function make_side() {
    const side = document.createElement('div');
    side.setAttribute('id', 'side');
    
    const img = document.createElement('img');
    img.setAttribute('src', 'http://4tccc.mooo.com/4TCCC.png');
    img.setAttribute('alt', '4TCCC logo');
    img.setAttribute('width', '200');
    img.setAttribute('height', '200');
    
    const timer = document.createElement('div');
    timer.setAttribute('id', 'timer');
    timer.innerHTML = 'time till webpage expires: 60 minutes';
    
    const credits = document.createElement('div');
    credits.innerHTML = 'webpage made for 4TCCC by epicalex4444';
    
    document.body.appendChild(side);
    side.appendChild(img);
    side.appendChild(timer);
    side.appendChild(credits);
}

function remove_side() {
    const side = document.getElementById('side');
    side.parentNode.removeChild(side);
}

//state tracking is used as side panel code on resizing only needs to update between state transmissions
let currState = is_mobile();
let lastState = currState;

//setup the webpage, side panel needs to be handled differenty if mobile
if (currState) {
    remove_side();
} else {
    setup_side();
}
setup_webpage(currState);

//handles window resizing
window.addEventListener('resize', function() {
    lastState = currState;
    currState = is_mobile();

    //adds or removes side panel if there is a mode transistion
    if (currState != lastState) {
        if (currState) {
            remove_side();
        } else {
            make_side();
            setup_side();
        }
    }

    setup_webpage(currState);
});

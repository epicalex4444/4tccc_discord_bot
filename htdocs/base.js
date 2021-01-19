/*
known bugs:
3 line + titles create 1 pixel of scrolling, no idea
no title breaks the webpage, no idea
website completely broken on mobile but mobile mode works on desktop fine, probably browser support issue
*/

const windowHeight = $(window).height();
const windowWidth = $(window).width();
const fontWidth = 8; //16px monospace is 8px wide
const lineHeight = 14;

//determine if it is being displayed on mobile or not, mobile just means small viewport in this instance
const mobile = false;
if (windowWidth < 1000) {
    mobile = true;
}

function getScrollbarWidth() {
    const outer = document.createElement('div');
    outer.style.visibility = 'hidden';
    outer.style.overflow = 'scroll';
    outer.style.msOverflowStyle = 'scrollbar';
    document.body.appendChild(outer);
    const inner = document.createElement('div');
    outer.appendChild(inner);
    const scrollbarWidth = (outer.offsetWidth - inner.offsetWidth);
    outer.parentNode.removeChild(outer);
    return scrollbarWidth;
}

const scrollbarWidth = getScrollbarWidth();

$(document).ready(function() {
    //set height of main and numbers
    const headerHeight = $('header').outerHeight();
    const bodyHeight = windowHeight - headerHeight;
    let scrollbar = true;
    let mainHeight = $('main').outerHeight();
    if (bodyHeight > $('main').outerHeight()) {
        scrollbar = false;
        mainHeight = bodyHeight;
    }
    $('main').outerHeight(mainHeight);
    $('numbers').outerHeight(mainHeight);

        //adds the numbers to numbers
        let numbersText = '';
        const lineLength = $('main').width();
        let mainText = $('main').text().split('\n');
        if (mainText[0] == '') {mainText = [$('main').text()];}
        if (mainText[0] == '') {mainText = [];}
        let lineNum = 0;
        let totalLines = 0;
        const minimumLines = Math.floor(mainHeight / lineHeight);
    
        for (; lineNum < mainText.length; ++lineNum) {
            numbersText += String(lineNum + 1) + '\n';
    
            linesTaken = Math.ceil(fontWidth * mainText[lineNum].length / lineLength);
            for (let _ = 1; _ < linesTaken; ++_) {
                numbersText += '\n';
                ++totalLines;
            }
    
            ++totalLines;
        }
    
        for (; totalLines < minimumLines; ++totalLines) {
            numbersText += String(lineNum + 1) + '\n';
            ++lineNum;
        }
    
        $('numbers').text(numbersText.substring(0, numbersText.length - 1));

    //sets up different webpage depending on whether it is being displayed on mobile or not
    if (!mobile) {
        //add min width of 4 digtis to numbers
        $('numbers').css('min-width', '44px');

        //add side panel
        $('body').append('<side></side>');
        const img = '<img src="http://4tccc.mooo.com/4tccc.png" alt="4TCCC logo" width="220" height="220"></img>';
        const timer = '<timer></timer>'
        const p = '<p>webpage made for 4TCCC by epicalex4444</p>'
        $('side').append(img, timer, p);

        const numbersWidth = $('numbers').outerWidth();
        const sideWidth = $('side').outerWidth();

        //set width of main
        if (scrollbar) {
            $('main').outerWidth(windowWidth - numbersWidth - sideWidth - scrollbarWidth);
        } else {
            $('main').outerWidth(windowWidth - numbersWidth - sideWidth);
        }

        //offset main
        $('main').css('left', numbersWidth);

        //set height of side
        const sideHeight = Math.min(windowHeight, mainHeight);
        $('side').outerHeight(sideHeight);

        //countdown timer
        const timeCreated = Math.floor($('meta[name=timeCreated]').attr('content') / 60);
        const currTime = Math.floor(new Date().getTime() / 60000);
        let minsRemaining = Math.max(0, 60 - (currTime - timeCreated));
        $('timer').text('time till webpage expires: ' + String(Math.max(0, minsRemaining)) + ' minutes');
        if (minsRemaining != 0) {
            setInterval(function() {
                minsRemaining -= 1;
                $('timer').text('time till webpage expires: ' + String(Math.max(0, minsRemaining)) + ' minutes');
            }, 60000);
        }
    } else {
        const numbersWidth = $('numbers').outerWidth();
        console.log(numbersWidth);

        //set width of main
        if (scrollbar) {
            $('main').outerWidth(windowWidth - numbersWidth - scrollbarWidth);
        } else {
            $('main').outerWidth(windowWidth - numbersWidth);
        }

        //offset main
        $('main').css('left', numbersWidth);
    }
});

//mobile mode doesn't have a side panel no special scrolling functionality is needed 
if (!mobile) {
    //makes side panel stop scrolling down once the header is not visible
    $(document).scroll(function() {
        const headerHeight = $('header').outerHeight();
        if ($(document).scrollTop() > headerHeight) {
            $('side').css('position', 'fixed');
            $('side').css('top', 0);
        } else {
            $('side').css('position', 'absolute');
            $('side').css('top', headerHeight);
        }
    });
}

const path = require("path")
const fs = require("fs")

const pathToReadFile = path.join(path.resolve(), 'Recorded.txt');
const textContent = fs.readFileSync(pathToReadFile, 'utf-8');
console.log(textContent);
console.log('\n\n');
let correctedText = '';
for(let i=0; i<textContent.length; i++){
    if (textContent[i] == '['){
        for(let j=i+1; j<textContent.length; j++){
            if(textContent[j] == ']'){
                let tempStr = textContent.slice(i+1, j);
                console.log(i + '\t' + j);
                console.log(tempStr);

                //comment out to exclude effect of shift on letters. Need to modify to change string to uppercase or lowercase
                /* if(tempStr=='SHIFT'){
                    if(textContent[j+1] == textContent[j+1].toLowerCase()){
                        textContent[j+1].toUpperCase();
                        console.log(textContent[j+1]+'\n');
                    }
                    else if(textContent[j+1] == textContent[j+1].toUpperCase()){
                        textContent[j+1] = textContent[j+1].toLowerCase();
                    }
                } */

                if(tempStr == 'BACKSPACE'){
                    correctedText = correctedText.slice(0, correctedText.length-1);
                }
                i = j;
                break;
            }
        }
    }
    else{
        correctedText += textContent[i];
    }
}
console.log(correctedText);
pathToWriteFile = fs.readFileSync(path.join(path.resolve(), 'corrected-txt.txt'));
fs.writeFileSync('./corrected-txt.txt', correctedText);
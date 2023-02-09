

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**enforces constraints for an input of type text that forces the entry 
 * of values between 0 and 1 to be accepted. 
 * 
 * precision of 2 decimal points. 
 * 
 * e.g 0.65 is accepted but not 0.655.
*/

function PercSplitConstraintsEnforcer(event) {
    const inp = event.target
    inp.value = inp.value.replace(/[^0-9.]/g, '');
    if (inp.value !== "") {
        // if not number
        if (isNaN(inp.value)) {
            inp.value = "0"
        } 
        // if is number 
        else {
            // if less than 0 set as 0
            if (inp.value < 0) {
                inp.value = 0;
            }
            // if greater than 1 set as 1
            else if (inp.value >= 1) {
                inp.value = 1;
            } 
            // if length is > 4, trim
            else if (inp.value.length > 4) {
                inp.value = inp.value.slice(0, -1)
            }
        }
    }
}


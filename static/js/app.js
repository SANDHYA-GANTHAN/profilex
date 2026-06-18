// Skill Chip Input

let skills = [];

const skillInput =
document.getElementById("skill-input");

const skillsContainer =
document.getElementById("skills-container");

if(skillInput){

    skillInput.addEventListener(
        "keydown",
        e => {

            if(e.key === "Enter"){

                e.preventDefault();

                let value =
                skillInput.value.trim();

                if(value){

                    let chip =
                    document.createElement("div");

                    chip.className =
                    "skill-chip";

                    chip.innerHTML =
                    value +
                    '<span>x</span>';

                    skills.push(value);

                    const hiddenInput =
                    document.getElementById(
                        "required_skills"
                    );

                    if(hiddenInput){
                        hiddenInput.value =
                        skills.join(",");
                    }

                    chip.querySelector("span")
                    .addEventListener(
                        "click",
                        ()=>{

                            chip.remove();

                            skills =
                            skills.filter(
                                s => s !== value
                            );

                            if(hiddenInput){
                                hiddenInput.value =
                                skills.join(",");
                            }

                        }
                    );

                    skillsContainer
                    .appendChild(chip);

                    skillInput.value = "";

                }

            }

        }
    );

}


// Upload Preview

const fileInput =
document.getElementById("fileInput");

const fileList =
document.getElementById("file-list");

if(fileInput){

    fileInput.addEventListener(
        "change",
        ()=>{

            fileList.innerHTML = "";

            for(let file of fileInput.files){

                let row =
                document.createElement("div");

                row.className =
                "file-card";

                row.innerHTML = `
                    <div>${file.name}</div>
                    <div class="spinner"></div>
                `;

                fileList.appendChild(row);

            }

        }
    );

}


// Drag & Drop

const dropzone =
document.getElementById("dropzone");

if(dropzone && fileInput){

    dropzone.onclick = ()=>{

        fileInput.click();

    };

    dropzone.addEventListener(
        "dragover",
        e=>{

            e.preventDefault();

            dropzone.style.background =
            "#eef0ff";

        }
    );

    dropzone.addEventListener(
        "dragleave",
        ()=>{

            dropzone.style.background =
            "white";

        }
    );

    dropzone.addEventListener(
        "drop",
        e=>{

            e.preventDefault();

            fileInput.files =
            e.dataTransfer.files;

        }
    );

}
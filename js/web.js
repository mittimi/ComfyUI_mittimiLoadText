import { ComfyApp, app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";


var allow_set_flag = true;


app.registerExtension({
	name: "ComfyUI_mittimiLoadText",
    
    async beforeConfigureGraph() {
        allow_set_flag = false;
    },
    
    async nodeCreated(node) {
        
        function send_message(node_id, message) {
            const body = new FormData();
            body.append('message',message);
            body.append('node_id', node_id);
            api.fetchApi("/mittimi_promptonly_path", { method: "POST", body, });
        }
        
        if (node.comfyClass == "LoadPromptMittimi") {
            
            Object.defineProperty(node.widgets[0], "value", {
                
                set: (value) => {
                    node._value = value;
                    if (allow_set_flag) send_message(node.id, value);
                },
                get: () => {
                    return node._value;
    			}
    		});
            
            function messageHandler(event) {
                
                if (node.id == event.detail.node) {
                    
                    if (event.detail.message['PositivePrompt']) node.widgets[1].value = event.detail.message['PositivePrompt'];
                    else if (event.detail.message['text']) node.widgets[1].value = event.detail.message['text'];
                    else node.widgets[1].value = "";
                    node.widgets[2].value = (event.detail.message['NegativePrompt'])?event.detail.message['NegativePrompt']:"";
                }
            }
            api.addEventListener("my.custom.message", messageHandler);
        }
        
        else if (node.comfyClass == "LoadTextMittimi") {
            
            Object.defineProperty(node.widgets[0], "value", {
                
                set: (value) => {
                    node._value = value;
                    if (allow_set_flag) send_message(node.id, value);
                },
                get: () => {
                    return node._value;
    			}
    		});
            
            function messageHandler(event) {

                if (node.id == event.detail.node) {

                    if (event.detail.message['text']) node.widgets[1].value = event.detail.message['text'];
                    else if (event.detail.message['PositivePrompt']) node.widgets[1].value = event.detail.message['PositivePrompt'];
                    else node.widgets[1].value = ""
                }
            }
            api.addEventListener("my.custom.message", messageHandler);
        }
    },
    
    async afterConfigureGraph() {
        allow_set_flag = true;
    }
});



    
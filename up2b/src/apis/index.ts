// @ts-nocheck
import { ImageBedsResponse } from "./interfaces"

function showImageBeds(callback: (r: ImageBedsResponse) => void) {
    pywebview.api.show_image_beds().then((response: ImageBedsResponse) => {
        callback(response)
    })
}

function initImageBeds() {}

export { showImageBeds }
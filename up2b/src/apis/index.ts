import {
    Pywebview,
    ImageBedsResponse,
    InitImageBedResponse,
    InitCommonImageBedParams,
    InitGitImageBedParams
} from './interfaces'

export function showImageBeds(callback: (r: ImageBedsResponse) => void) {
    // @ts-ignore
    const p = pywebview as Pywebview
    p.api.show_image_beds().then((response: ImageBedsResponse) => {
        callback(response)
    })
}

export function initImageBeds(data: InitCommonImageBedParams | InitGitImageBedParams, callback: (r: InitImageBedResponse) => void) {
    // @ts-ignore
    const p = pywebview as Pywebview
    p.api.init_image_bed(data).then((response: InitImageBedResponse) => {
        callback(response)
    })
}

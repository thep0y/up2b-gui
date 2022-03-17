import {
    Pywebview,
    ImageBedsResponse,
    CommonResponse,
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

export function initImageBeds(data: InitCommonImageBedParams | InitGitImageBedParams, callback: (r: CommonResponse) => void) {
    // @ts-ignore
    const p = pywebview as Pywebview
    p.api.init_image_bed(data).then((response: CommonResponse) => {
        callback(response)
    })
}

export function chooseImageBed(imageBedCode: number, callback: (r: CommonResponse) => void) {
    // @ts-ignore
    const p = pywebview as Pywebview
    p.api.choose_image_bed(imageBedCode).then((response: CommonResponse) => {
        callback(response)
    })
}

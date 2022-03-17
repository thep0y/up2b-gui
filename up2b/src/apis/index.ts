import axios from 'axios'
import {
    Pywebview,
    ImageBedsResponse,
    CommonResponse,
    InitCommonImageBedParams,
    InitGitImageBedParams
} from './interfaces'

export function showImageBeds(callback: (r: ImageBedsResponse) => void) {
    axios.get('/getImageBeds').then(r => {
        const resp: ImageBedsResponse = r.data
        callback(resp)
    })
}

export function initImageBeds(data: InitCommonImageBedParams | InitGitImageBedParams, callback: (r: CommonResponse) => void) {
    axios.post('/init', data, { headers: { 'Content-Type': 'application/json' } }).then(r => {
        const resp: CommonResponse = r.data
        callback(resp)
    })
}

export function chooseImageBed(imageBedCode: number, callback: (r: CommonResponse) => void) {
    axios.get('/chooseImageBed/' + imageBedCode).then(r => {
        const resp: CommonResponse = r.data
        callback(resp)
    })
}

export function toggleAutomaticCompression(ok: number, callback: (r: CommonResponse) => void) {
    axios.get('/ac/' + ok).then(r => {
        const resp: CommonResponse = r.data
        callback(resp)
    })
}

export function dragFile(file: any, callback: (r: CommonResponse) => void) {
    // @ts-ignore
    const p = pywebview as Pywebview
    p.api.drag_file(file).then((response: CommonResponse) => {
        callback(response)
    })
}

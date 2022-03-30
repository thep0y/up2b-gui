import axios from 'axios'
import type {
    ImageBedsResponse,
    CommonResponse,
    InitCommonImageBedParams,
    InitGitImageBedParams,
    PreviewRequest,
    ImageListResponse,
    DeleteParamsType,
    ACResponse
} from './interfaces'

type Method = 'GET' | 'POST'

const request = (url: string, method: Method, data?: string) => {
    return axios.request({
        url: import.meta.env.VITE_APP_BASE_API + url,
        method: method,
        data: data,
        headers: method == 'GET' ? undefined : { 'Content-Type': 'application/json' }
    })
}

export function showImageBeds(callback: (r: ImageBedsResponse) => void) {
    request('/getImageBeds', 'GET').then(r => {
        const resp: ImageBedsResponse = r.data
        callback(resp)
    })
}

export function initImageBeds(data: InitCommonImageBedParams | InitGitImageBedParams, callback: (r: CommonResponse) => void) {
    request('/init', 'POST', JSON.stringify(data)).then(r => {
        const resp: CommonResponse = r.data
        callback(resp)
    })
}

export function chooseImageBed(imageBedCode: number, callback: (r: CommonResponse) => void) {
    request('/chooseImageBed/' + imageBedCode, 'GET').then(r => {
        const resp: CommonResponse = r.data
        callback(resp)
    })
}

export function toggleAutomaticCompression(ok: number, callback: (r: ACResponse) => void) {
    request('/ac/' + ok, 'GET').then(r => {
        const resp: ACResponse = r.data
        callback(resp)
    })
}

export function previewInNewWindow(r: PreviewRequest, callback: (r: CommonResponse) => void) {
    request('/preview', 'POST', JSON.stringify(r)).then(r => {
        const resp: CommonResponse = r.data
        callback(resp)
    })
}

export function getAllImages(callback: (r: ImageListResponse) => void) {
    request('/getAllImages', 'GET').then(r => {
        const resp: ImageListResponse = r.data

        const ts = new Date().getTime();

        resp.urls.forEach(v => {
            v.url = v.url + '?ts=' + ts
        })

        callback(resp)
    })
}

export function deleteImage(params: DeleteParamsType, callback: (r: ImageListResponse) => void) {
    request('/delete', 'POST', JSON.stringify(params)).then(r => {
        const resp: ImageListResponse = r.data
        callback(resp)
    })
}

export * from './consts'
export * from './interfaces'
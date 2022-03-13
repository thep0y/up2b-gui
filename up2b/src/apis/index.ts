// @ts-nocheck

interface ImageBedsResponse {
    auth_data: Array<Object>,
    beds: { [key: string]: number },
    selected: number,
    screensize: { height: number, width: number }
}

function showImageBeds(callback: (r: ImageBedsResponse) => void) {
    pywebview.api.show_image_beds().then((response: ImageBedsResponse) => {
        callback(response)
    })
}

interface CommonConfig {
    username: string
    password: string
}

interface GitConfig {
    token: string
    username: string
    repo: string
    folder: string
}

export { ImageBedsResponse, showImageBeds, CommonConfig, GitConfig }
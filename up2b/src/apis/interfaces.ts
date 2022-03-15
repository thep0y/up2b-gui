interface ImageBedsResponse {
    auth_data: Array<Object>,
    beds: { [key: string]: number },
    selected: number,
    screensize: { height: number, width: number }
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

export { ImageBedsResponse, CommonConfig, GitConfig }
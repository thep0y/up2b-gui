export interface AuthDataItem {
    // 响应字段不是只有 type，只是响应里直接用到的共同字段只有 type
    type: number
}

export interface ImageBedsResponse {
    auth_data: Array<AuthDataItem>,
    beds: { [key: string]: number },
    selected: number,
    screensize: { height: number, width: number }
}

export interface CommonResponse {
    success: boolean,
    error: string
}

export interface UploadResponse {
    success: boolean
    error: string | Object
    url: string
    image: string
}

export interface CommonConfig {
    username: string
    password: string
}

export interface ErrorResponse {
    success: boolean
    error: {
        error: string
        image_path: string
        status_code: number
    }
}

export interface GitConfig {
    token: string
    username: string
    repo: string
    folder: string
}

export interface InitCommonImageBedParams extends CommonConfig {
    'image-bed': number
}

export interface InitGitImageBedParams extends GitConfig {
    'image-bed': number
}

export interface Tag {
    index: number,
    name: string,
    effect: import('element-plus/es/utils').BuildPropType<StringConstructor, 'plain' | 'light' | 'dark', unknown>
}

export interface PreviewRequest {
    url: string
    width: number
    height: number
}

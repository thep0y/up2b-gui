export interface Pywebview {
    token: string,
    platform: string,
    api: Api
}

export interface ImageBedsResponse {
    auth_data: Array<Object>,
    beds: { [key: string]: number },
    selected: number,
    screensize: { height: number, width: number }
}

export interface InitImageBedResponse {
    success: boolean,
    error: string
}

export interface CommonConfig {
    username: string
    password: string
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

abstract class Api {
    abstract show_image_beds(): Promise<ImageBedsResponse>
    abstract init_image_bed(data: InitCommonImageBedParams | InitGitImageBedParams): Promise<InitImageBedResponse>
}
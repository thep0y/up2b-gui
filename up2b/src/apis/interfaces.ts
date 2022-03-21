export type ImageBedType = 1 | 2

export interface ImageBedsResponse {
    types: Array<ImageBedType>,
    save_beds: Array<number>,
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

export interface ErrorObject {
    error: string
    image_path: string
    status_code: number

}

export interface ErrorResponse {
    success: boolean
    error: string | ErrorObject
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

export interface SMMSDeleteParams {
    delete_url: string
}

export interface ImgtuDeleteParams {
    id: string
}

export interface GitDeleteParams {
    sha: string
    delete_url: string
}

export interface SMMSImageListItem extends SMMSDeleteParams {
    url: string
    width: number
    height: number
}

export interface ImgtuImageListItem extends ImgtuDeleteParams {
    url: string
    display_url: string
    width: number
    height: number
}

export interface GitImageListItem extends GitDeleteParams {
    url: string
}

export type DeleteParamsType = SMMSDeleteParams | ImgtuDeleteParams | GitDeleteParams

export type ImageListItemType = SMMSImageListItem | ImgtuImageListItem | GitImageListItem

export type ImageListType = Array<ImageListItemType>

export interface ImageListResponse extends ErrorResponse {
    urls: ImageListType
}

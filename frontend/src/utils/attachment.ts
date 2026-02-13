export function getFileIcon(url: string): string {
    const ext = url.split(".").pop()?.toLowerCase() ?? "";
    if (["jpg","jpeg","png","gif","webp"].includes(ext)) return "mdi:image-outline";
    if (ext === "pdf") return "mdi:file-pdf-box";
    return "mdi:file-document-outline";
}

export function getFileName(url: string): string {
    return url.split("/").pop() ?? url;
}

export function isImage(url: string): boolean {
    const ext = url.split(".").pop()?.toLowerCase() ?? "";
    return ["jpg","jpeg","png","gif","webp"].includes(ext);
}
# SpotDL-Syncer

Un "ecosistema" de scripts de Python para crear y mantener sincronizadas múltiples Playlists/Albumes de Spotify.

> Potenciado por [spotDL](https://github.com/spotDL/spotify-downloader)

## Dependencias

- [Python 3.8](https://www.python.org/downloads/)
	- [spotDL](https://github.com/spotDL/spotify-downloader)

## Uso

Es importante mencionar que, dependiendo de donde ejecutes el script, se llevarán a cabo todas las operaciones, como descargar y sincronizar las listas de reproducción. Además, ten en cuenta que este programa funciona como un "ecosistema", por lo que todas las carpetas de Playlists deben almacenarse en `main` o junto a los scripts.

**Durante esta guía, toma en nota esto:**

-   "Playlist" también se refiere a "Playlist/Album"
-   La carpeta `main` puede ser renombrada a cualquier cosa, pero los scripts deben mantenerse en la misma carpeta.

### Sincronizar nueva Playlist

1. Ejecuta `new-playlist.py`
2. Ingresa una URL valida de Spotify (Playlist/Album) y sigue las instrucciones. Una carpeta con el nombre de la Playlist se creara en el mismo directorio del script.
3. Para sincronizar únicamente esta Playlist entra en su carpeta y ejecuta `sync-playlist`.

**ADVERTENCIA**: no elimines ni muevas el archivo `data.spotdl` de la carpeta o romperás la sincronización!

### Sincronizar todas las Playlists

Para sincronizar todas las Playlist descargadas,:

1. En `main`, ejecuta `sync-all`.
2. Espera a que el programa sincronice todas las Playlist descargadas en todos los directorios, puede tardar un rato.

**ADVENTENCIA**: la sincronización removerá cualquier archivo de música que no se encuentre en la Playlist de Spotify, por lo tanto, no almacene archivos 
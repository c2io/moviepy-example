from pathlib import Path

import typer
import moviepy.editor as mpe
import gizeh
from loguru import logger

app = typer.Typer()


@app.command()
def cut_and_add(
    from_filename: str,
    from_second_start: int = 0,
    from_second_end: int = 60,
    total_second: int = 120,
    to_filename: str = "temp/to-120s.mp4",
):
    logger.debug(
        f"{from_filename},{from_second_start},{from_second_end},{total_second},{to_filename}"
    )

    video_file_clip = mpe.VideoFileClip(from_filename)
    width, height = video_file_clip.size

    def make_frame(t):
        duration = 2
        t = t % duration

        radius = min(width, height) * (1 + (t * (duration - t)) ** 2) / 6
        circle = gizeh.circle(radius, xy=(width / 2, height / 2), fill=(1, 0, 0))

        surface = gizeh.Surface(width, height)
        circle.draw(surface)

        return surface.get_npimage()

    video_clip = mpe.VideoClip(make_frame)

    video = mpe.concatenate_videoclips(
        [
            video_file_clip.subclip(from_second_start, from_second_end),
            video_clip.set_duration(
                total_second - (from_second_end - from_second_start)
            ),
        ]
    )

    Path(to_filename).parent.mkdir(exist_ok=True, parents=True)
    video.write_videofile(to_filename, audio=False)


if __name__ == "__main__":
    app()

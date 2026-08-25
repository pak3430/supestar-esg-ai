/**
 * Composition — scenes.ts 가 시간축을 소유한다.
 * 오디오는 public/audio/{01..}.mp3 가 있으면 자동으로 붙는다.
 */
import React from 'react';
import { Composition, Sequence, AbsoluteFill, Audio, staticFile } from 'remotion';
import { SCENES, FPS, WIDTH, HEIGHT, frames, totalFrames } from './scenes';
import { SceneView } from './Film';
import { BG } from './design';

const LEAD_SEC = 0.5;      // 장면 시작 후 음성이 들어가기까지의 여유

const Film: React.FC<{ hasAudio: boolean }> = ({ hasAudio }) => {
  let acc = 0;
  return (
    <AbsoluteFill style={{ background: BG }}>
      {SCENES.map((s, i) => {
        const from = frames(acc);
        acc += s.durationSec;
        return (
          <Sequence key={s.id} from={from} durationInFrames={frames(s.durationSec)}>
            <SceneView scene={s} />
            {hasAudio && (
              <Sequence from={frames(LEAD_SEC)}>
                <Audio src={staticFile(`audio/${String(i + 1).padStart(2, '0')}.mp3`)} />
              </Sequence>
            )}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="FilmNarrated" component={Film} defaultProps={{ hasAudio: true }}
      durationInFrames={totalFrames()} fps={FPS} width={WIDTH} height={HEIGHT}
    />
    <Composition
      id="FilmSilent" component={Film} defaultProps={{ hasAudio: false }}
      durationInFrames={totalFrames()} fps={FPS} width={WIDTH} height={HEIGHT}
    />
  </>
);

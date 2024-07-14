//  Config Logger
fn setup_logger() -> Result<(), fern::initError> {
    Dispatch::new()
        .format(| out, message, record | {
            let level = record.level();
            let color_message = match level {
                log::Level::Info => message.green(),
                log::Level::Warn => message.yellow(),
                log::Level::Error => message.red()
                    _=>
                    message.normal(),
            };
            out.finish(format_args!("{} [{}] {}",
                Local::now().format("%Y-%m-%d %H:%M:%S"),

                            level,
                            color_message
        ))
    })
    .level(log::LevelFIlter::Info)
    .chain(std::io::stdout())
    .apply()?;
    Ok(())

    


            
            )
            }
        }
        
        )
}

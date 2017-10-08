#!/usr/bin/env python3

import os
import click

import grex.seed
import grex.store
import grex.config

@click.group("cetest")
@click.option("-s","--store",
              default=lambda: os.environ.get('GREX_STORE', "sqlite:///:memory:"))
@click.pass_context
def cli(ctx, store):
    click.echo("using store: %s" % repr(store))

    if store == ":memory:" or ":" not in store:
        store = "sqlite:///" + store

    ctx.obj['store'] = store
    ctx.obj['session'] = grex.store.session(store)

    pass


@cli.command("seed")
@click.option("--save/--no-save", default=True, help="Save new seeds in the store.")
@click.argument("host")
@click.pass_context
def seed(ctx, save, host):
    '''
    Find new seeds.
    '''
    seeds = grex.seed.by_host(host)

    ses = ctx.obj['session']
    have = ses.query(grex.store.DaqRun).filter_by(host=host)
        
    # fixme: this is maybe slower than it could be.
    new_seeds = list()
    for seed in seeds:
        got = have.filter_by(datadir=seed['datadir']).all()
        if not got:
            new_seeds.append(seed)
    if not new_seeds:
        click.echo("no new seeds")
        return
    else:
        click.echo("found %d new seeds" % len(new_seeds))
    if not save:
        return
    for seed in new_seeds:
        s = grex.store.DaqRun(**seed)
        ses.add(s)
        print ("Adding seed: %s" % repr(s))
    ses.commit()
    return

@cli.command("run")
@click.option("-g","--graph",
              help="A command graph in the form of a Jsonnet file")
@click.argument("seeds", nargs=-1) # list of seed ID numbers of ident strings
@click.pass_context
def run(ctx,graph,seeds):
    '''
    Run a command graph against seeds.
    '''
    if not seeds:
        click.echo("no seeds given")
        return
    ses = ctx.obj['session']
    seed_obj = list()
    for sid in seeds:
        try:
            sid = int(sid)
            obj = ses.query(grex.store.DaqRun).filter_by(id=sid).all()
        except ValueError:
            h,cat,cfg,ts = sid.split('-')
            obj = ses.query(grex.store.DaqRun).filter_by(host=h,category=cat,config=cfg,timestamp=ts).all()
        if not obj:
            click.echo("no such seed: %s" % repr(sid))
            continue
        if len(obj) > 1:
            click.echo("got multiple seeds for %s, using first" % repr(sid))
        seed_obj.append(obj[0])

    for seed in seed_obj:
        print (seed.asdict())
        #one = grex.config.loads(gtext, **seed.asdict())
        #grex.graph.execute(one)
    
            


def main():
    cli(obj=dict())

if '__main__' == __name__:
    main()



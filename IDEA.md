# The idea, in Ahmed's words

Typed on the box, 2026-10-13 16:52 (Oman), session `386e4166` in `~/.forge/genesis`:

> kinda lost passion and a bit of a burnout but i have an idea, i was today reesearching a bit about ebms and i
> was thinking what if we make a small nural network made out of smaller pretrained energy based models theat has
> one job thatr is to make connections, each connection makes another connection and each pattern of connection
> does an action, each action and connection gets cashes and each small model gets retrained again at sleep for
> the morning and it grows over generations

And 16:55:

> i want to try this outside of our genises project but i want your knowaldge and experments and root, you my
> friend have a quality i admire, you never faked a number (i hope) everything is well made nothing is syntitc

And on the laptop, 2026-10-13:

> i want to experment with it and learn it very deeply with you, this is gonna be soo much fun <3 :D

## The parts, pulled apart (Claude's reading; to be confirmed with Ahmed)

1. **Units**: many SMALL energy-based models, pretrained.
2. **One job**: make connections (each unit scores "does this link belong?" as an energy).
3. **Cascade**: each connection makes another connection (growth / spreading activation).
4. **Patterns -> actions**: a recognisable pattern of connections triggers an action.
5. **Cache**: actions and connections are recorded during the "day".
6. **Sleep**: each small model is retrained on the cache overnight (consolidation / replay).
7. **Generations**: the whole thing grows over generations.

Open: what is the world / task the actions act on? what is "pretrained" on? what does a generation mean
(a sleep cycle? a reproduction step?)? what counts as success?

## Ahmed's insight, 2026-10-13 (laptop, after thinking it through)

> so the creature doesnt spawn knowing what food is, its body and the chemtery teach it, everything is made
> out of chemestry thats why everything in the rel world blends together and we trying to model it with
> numbers is difficult to imagine let alone implemnt

Design consequence (Claude): no "food" label anywhere in the code. The teacher is the body's own
chemistry: eat something, and an internal quantity moves toward or away from its setpoint. Smells are
blends of a few chemical "notes", so food and poison can share notes.

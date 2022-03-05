from plugins.Args import Args
import os
from helper import *
def startGenerating(args:Args):
    prompts = args.prompts
    size = [int(args.width), int(args.height)]
    noise_prompt_seeds=[]
    noise_prompt_weights=[]
    modelo = args.model
    nombre_modelo = modelo

    if modelo == "gumbel_8192":
        is_gumbel = True
    else:
        is_gumbel = False

    vqgan_config=f'{os.path.abspath(".")}/models/{modelo}.yaml'
    vqgan_checkpoint=f'{os.path.abspath(".")}/models/{modelo}.ckpt'
    clip_model='ViT-B/32'
    display_freq=int(args.interval_image)
    init_image = ""
    image_prompts = ""
    imagenes_objetivo = image_prompts
    init_weight=0.
    seed = int(args.seed)
    max_iterations = int(args.max_iterations)
    max_iteraciones = max_iterations
    input_images = ""
    step_size=0.1
    cutn = 64
    cut_pow = 1.

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print('Using device:', device)
    if prompts:
        print('Using texts:', prompts)
    if imagenes_objetivo:
        print('Using image prompts:', imagenes_objetivo)
    if seed is None:
        seed = torch.seed()
    else:
        seed = seed
    torch.manual_seed(seed)
    print('Using seed:', seed)

    model = load_vqgan_model(vqgan_config, vqgan_checkpoint).to(device)
    perceptor = clip.load(clip_model, jit=False)[0].eval().requires_grad_(False).to(device)

    cut_size = perceptor.visual.input_resolution
    if is_gumbel:
        e_dim = model.quantize.embedding_dim
    else:
        e_dim = model.quantize.e_dim

    f = 2**(model.decoder.num_resolutions - 1)
    make_cutouts = MakeCutouts(cut_size, cutn, cut_pow=cut_pow)
    if is_gumbel:
        n_toks = model.quantize.n_embed
    else:
        n_toks = model.quantize.n_e

    toksX, toksY = size[0] // f, size[1] // f
    sideX, sideY = toksX * f, toksY * f
    if is_gumbel:
        z_min = model.quantize.embed.weight.min(dim=0).values[None, :, None, None]
        z_max = model.quantize.embed.weight.max(dim=0).values[None, :, None, None]
    else:
        z_min = model.quantize.embedding.weight.min(dim=0).values[None, :, None, None]
        z_max = model.quantize.embedding.weight.max(dim=0).values[None, :, None, None]

    if init_image:
        pil_image = Image.open(init_image).convert('RGB')
        pil_image = pil_image.resize((sideX, sideY), Image.LANCZOS)
        z, *_ = model.encode(TF.to_tensor(pil_image).to(device).unsqueeze(0) * 2 - 1)
    else:
        one_hot = F.one_hot(torch.randint(n_toks, [toksY * toksX], device=device), n_toks).float()
        if is_gumbel:
            z = one_hot @ model.quantize.embed.weight
        else:
            z = one_hot @ model.quantize.embedding.weight
        z = z.view([-1, toksY, toksX, e_dim]).permute(0, 3, 1, 2)
    z_orig = z.clone()
    z.requires_grad_(True)
    opt = optim.Adam([z], lr=step_size)

    normalize = transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073],
                                    std=[0.26862954, 0.26130258, 0.27577711])

    pMs = []

    for prompt in prompts:
        txt, weight, stop = parse_prompt(prompt)
        embed = perceptor.encode_text(clip.tokenize(txt).to(device)).float()
        pMs.append(Prompt(embed, weight, stop).to(device))

    for prompt in image_prompts:
        path, weight, stop = parse_prompt(prompt)
        img = resize_image(Image.open(path).convert('RGB'), (sideX, sideY))
        batch = make_cutouts(TF.to_tensor(img).unsqueeze(0).to(device))
        embed = perceptor.encode_image(normalize(batch)).float()
        pMs.append(Prompt(embed, weight, stop).to(device))

    for seed, weight in zip(noise_prompt_seeds, noise_prompt_weights):
        gen = torch.Generator().manual_seed(seed)
        embed = torch.empty([1, perceptor.visual.output_dim]).normal_(generator=gen)
        pMs.append(Prompt(embed, weight).to(device))

    def synth(z):
        if is_gumbel:
            z_q = vector_quantize(z.movedim(1, 3), model.quantize.embed.weight).movedim(3, 1)
        else:
            z_q = vector_quantize(z.movedim(1, 3), model.quantize.embedding.weight).movedim(3, 1)
        
        return clamp_with_grad(model.decode(z_q).add(1).div(2), 0, 1)

    def add_xmp_data(nombrefichero):
        imagen = ImgTag(filename=nombrefichero)
        imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'creator', 'VQGAN+CLIP', {"prop_array_is_ordered":True, "prop_value_is_array":True})
        if prompts:
            imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'title', " | ".join(prompts), {"prop_array_is_ordered":True, "prop_value_is_array":True})
        else:
            imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'title', 'None', {"prop_array_is_ordered":True, "prop_value_is_array":True})
        imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'i', str(i), {"prop_array_is_ordered":True, "prop_value_is_array":True})
        imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'model', nombre_modelo, {"prop_array_is_ordered":True, "prop_value_is_array":True})
        imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'seed',str(seed) , {"prop_array_is_ordered":True, "prop_value_is_array":True})
        imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'input_images',str(input_images) , {"prop_array_is_ordered":True, "prop_value_is_array":True})
        #for frases in prompts:
        #    imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'Prompt' ,frases, {"prop_array_is_ordered":True, "prop_value_is_array":True})
        imagen.close()

    def add_stegano_data(filename):
        data = {
            "title": " | ".join(prompts) if prompts else None,
            "notebook": "VQGAN+CLIP",
            "i": i,
            "model": nombre_modelo,
            "seed": str(seed),
            "input_images": input_images
        }
        lsb.hide(filename, json.dumps(data)).save(filename)

    @torch.no_grad()
    def checkin(i, losses):
        losses_str = ', '.join(f'{loss.item():g}' for loss in losses)
        a = "-"
        tqdm.write(f'i: {i},\nloss: {sum(losses).item():g},\nlosses: {losses_str}\n{a*os.get_terminal_size().columns}')
        out = synth(z)
        TF.to_pil_image(out[0].cpu()).save('progress.png')
        add_stegano_data('progress.png')
        add_xmp_data('progress.png')
        # display.display(display.Image('progress.png'))

    i = 0
    def ascend_txt():
        # global i
        out = synth(z)
        iii = perceptor.encode_image(normalize(make_cutouts(out))).float()

        result = []

        if init_weight:
            result.append(F.mse_loss(z, z_orig) * init_weight / 2)

        for prompt in pMs:
            result.append(prompt(iii))
        img = np.array(out.mul(255).clamp(0, 255)[0].cpu().detach().numpy().astype(np.uint8))[:,:,:]
        img = np.transpose(img, (1, 2, 0))
        filename = f"./steps/{i:04}.png"
        imageio.imwrite(filename, np.array(img))
        add_stegano_data(filename)
        add_xmp_data(filename)
        return result

    def train(i):
        opt.zero_grad()
        lossAll = ascend_txt()
        if i % display_freq == 0:
            checkin(i, lossAll)
        loss = sum(lossAll)
        loss.backward()
        opt.step()
        with torch.no_grad():
            z.copy_(z.maximum(z_min).minimum(z_max))

    
    try:
        with tqdm() as pbar:
            while True:
                train(i)
                if i == max_iteraciones:
                    break
                i += 1
                pbar.update()
    except KeyboardInterrupt:
        pass